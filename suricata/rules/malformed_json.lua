-- malformed_json.lua

function init(args)
    local needs = {}
    needs["payload"] = tostring(true)  -- Request packet payload
    return needs
end

function match(args)
    local payload = args["payload"]
    if not payload then
        SCLogInfo("Lua: NO RAW PAYLOAD!")
        return 0
    end

    SCLogInfo("Lua: PAYLOAD = " .. payload)

    -- Detect malformed JSON: starts with `{` but missing closing `}`
    if string.match(payload, '{') and not string.find(payload, '}') then
        return 1
    end

    -- Detect trailing comma or incomplete quoted string
    if string.match(payload, '[,]$') or string.match(payload, '"[^"]*$') then
        return 1
    end

    return 0
end
