$utf8 = New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8

function Send-Json($message) {
    $json = ConvertTo-Json -InputObject $message -Depth 50 -Compress
    [Console]::Out.WriteLine($json)
    [Console]::Out.Flush()
}

function Send-Error($requestId, [int]$code, [string]$message) {
    Send-Json @{
        jsonrpc = "2.0"
        id = $requestId
        error = @{
            code = $code
            message = $message
        }
    }
}

while ($null -ne ($line = [Console]::In.ReadLine())) {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }

    try {
        $request = ConvertFrom-Json -InputObject $line -ErrorAction Stop
    }
    catch {
        Send-Error $null -32700 "Parse error"
        continue
    }

    $hasId = $request.PSObject.Properties.Name -contains "id"
    if ($request.jsonrpc -ne "2.0" -or [string]::IsNullOrWhiteSpace($request.method)) {
        if ($hasId) {
            Send-Error $request.id -32600 "Invalid request"
        }
        continue
    }

    switch ($request.method) {
        "initialize" {
            if ($hasId) {
                Send-Json @{
                    jsonrpc = "2.0"
                    id = $request.id
                    result = @{
                        protocolVersion = $request.params.protocolVersion
                        capabilities = @{
                            tools = @{}
                        }
                        serverInfo = @{
                            name = "echo-windows"
                            version = "1.0.0"
                        }
                    }
                }
            }
        }
        "notifications/initialized" { }
        "ping" {
            if ($hasId) {
                Send-Json @{ jsonrpc = "2.0"; id = $request.id; result = @{} }
            }
        }
        "tools/list" {
            if ($hasId) {
                Send-Json @{
                    jsonrpc = "2.0"
                    id = $request.id
                    result = @{
                        tools = @(
                            @{
                                name = "echo"
                                description = "Return the supplied message."
                                inputSchema = @{
                                    type = "object"
                                    properties = @{
                                        message = @{ type = "string"; description = "Message to echo." }
                                    }
                                    required = @("message")
                                }
                            },
                            @{
                                name = "calculate"
                                description = "Calculate two numbers using the selected arithmetic operation."
                                inputSchema = @{
                                    type = "object"
                                    properties = @{
                                        a = @{ type = "number"; description = "First operand." }
                                        b = @{ type = "number"; description = "Second operand." }
                                        operation = @{
                                            type = "string"
                                            enum = @("add", "subtract", "multiply", "divide")
                                            description = "Arithmetic operation to perform."
                                        }
                                    }
                                    required = @("a", "b", "operation")
                                    additionalProperties = $false
                                }
                            }
                        )
                    }
                }
            }
        }
        "tools/call" {
            if ($hasId) {
                $arguments = $request.params.arguments
                if ($request.params.name -eq "calculate") {
                    $calculationError = $null
                    $calculationResult = $null
                    $argumentNames = if ($null -ne $arguments) { $arguments.PSObject.Properties.Name } else { @() }
                    if ($null -eq $arguments -or -not ($argumentNames -contains "a") -or -not ($argumentNames -contains "b") -or -not ($argumentNames -contains "operation")) {
                        $calculationError = "The calculate tool requires numeric a and b values and an operation."
                    }
                    elseif (
                        (($arguments.a -isnot [byte]) -and ($arguments.a -isnot [int16]) -and ($arguments.a -isnot [int]) -and ($arguments.a -isnot [long]) -and ($arguments.a -isnot [single]) -and ($arguments.a -isnot [double]) -and ($arguments.a -isnot [decimal])) -or
                        (($arguments.b -isnot [byte]) -and ($arguments.b -isnot [int16]) -and ($arguments.b -isnot [int]) -and ($arguments.b -isnot [long]) -and ($arguments.b -isnot [single]) -and ($arguments.b -isnot [double]) -and ($arguments.b -isnot [decimal])) -or
                        ($arguments.operation -isnot [string])
                    ) {
                        $calculationError = "The calculate tool requires numeric a and b values and a string operation."
                    }
                    else {
                        $a = [double]$arguments.a
                        $b = [double]$arguments.b
                        if ([double]::IsNaN($a) -or [double]::IsInfinity($a) -or [double]::IsNaN($b) -or [double]::IsInfinity($b)) {
                            $calculationError = "Operands must be finite numbers."
                        }
                        else {
                            switch ($arguments.operation) {
                                "add" { $calculationResult = $a + $b }
                                "subtract" { $calculationResult = $a - $b }
                                "multiply" { $calculationResult = $a * $b }
                                "divide" {
                                    if ($b -eq 0) {
                                        $calculationError = "Cannot divide by zero."
                                    }
                                    else {
                                        $calculationResult = $a / $b
                                    }
                                }
                                default { $calculationError = "Unsupported operation: $($arguments.operation)" }
                            }
                        }
                    }

                    if ($calculationError) {
                        Send-Json @{
                            jsonrpc = "2.0"
                            id = $request.id
                            result = @{
                                isError = $true
                                content = @(@{ type = "text"; text = $calculationError })
                            }
                        }
                    }
                    else {
                        $formattedResult = $calculationResult.ToString("G", [System.Globalization.CultureInfo]::InvariantCulture)
                        Send-Json @{
                            jsonrpc = "2.0"
                            id = $request.id
                            result = @{
                                content = @(@{ type = "text"; text = $formattedResult })
                                structuredContent = @{ result = $calculationResult }
                            }
                        }
                    }
                }
                elseif ($request.params.name -eq "echo") {
                    if ($null -eq $arguments -or -not ($arguments.PSObject.Properties.Name -contains "message") -or $arguments.message -isnot [string]) {
                        Send-Json @{
                            jsonrpc = "2.0"
                            id = $request.id
                            result = @{
                                isError = $true
                                content = @(@{ type = "text"; text = "The echo tool requires a string message." })
                            }
                        }
                    }
                    else {
                        Send-Json @{
                            jsonrpc = "2.0"
                            id = $request.id
                            result = @{
                                content = @(@{ type = "text"; text = $arguments.message })
                            }
                        }
                    }
                }
                else {
                    Send-Json @{
                        jsonrpc = "2.0"
                        id = $request.id
                        result = @{
                            isError = $true
                            content = @(@{ type = "text"; text = "Unknown tool: $($request.params.name)" })
                        }
                    }
                }
            }
        }
        default {
            if ($hasId) {
                Send-Error $request.id -32601 "Method not found: $($request.method)"
            }
        }
    }
}