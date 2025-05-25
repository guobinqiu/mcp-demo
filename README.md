# MCP Python Demo

> LLM 使用的 `deepseek-chat` 因为只有v3有`tools`属性 (`deepseek-reasoner`是不行的)

```python
chat_response = client.chat.completions.create(
    model="deepseek-chat", # 通过指定 model='deepseek-chat' 即可调用 DeepSeek-V3 V3有tools属性
    messages=messages,
    tools=available_tools,
    tool_choice="auto"
)
```

## 安装

```
pip install uv
# uv init mcp-demo-python
git clone git@github.com:guobinqiu/mcp-demo-python.git
cd mcp-demo-python
uv venv
source .venv/bin/activate
# uv add "mcp[cli]" httpx
# uv add mcp openai python-dotenv
# rm main.py
```

## 运行

运行前把`.env`文件里的`OPENAI_API_KEY`换成你自己的

```
python3 client/main.py server/main.py
```

## 输出

```
[04/23/25 21:11:54] INFO     Processing request of type ListToolsRequest                                                                                 server.py:534

Connected to server with tools: ['get_alerts', 'get_forecast']

MCP Client Started!
Type your queries or 'quit' to exit.

Query: what's the weather in new york 
[04/23/25 21:12:09] INFO     Processing request of type ListToolsRequest                                                                                 server.py:534
[04/23/25 21:12:15] INFO     Processing request of type CallToolRequest                                                                                  server.py:534
                    INFO     HTTP Request: GET https://api.weather.gov/points/40.7128,-74.006 "HTTP/1.1 200 OK"                                        _client.py:1740
[04/23/25 21:12:16] INFO     HTTP Request: GET https://api.weather.gov/gridpoints/OKX/33,35/forecast "HTTP/1.1 200 OK"                                 _client.py:1740
[DEBUG] final_text[0] type: <class 'str'>, value: Here's the current weather forecast for New York:

### Today:  
- **Temperature:** 73°F  
- **Wind:** 7 mph NW  
- **Forecast:** Mostly sunny, with a high near 73.  

### Tonight:  
- **Temperature:** 57°F  
- **Wind:** 3 to 7 mph SE  
- **Forecast:** Mostly clear.  

### Thursday:  
- **Temperature:** 68°F (falling to 64°F in the afternoon)  
- **Wind:** 3 to 12 mph SE  
- **Forecast:** Sunny.  

### Thursday Night:  
- **Temperature:** 56°F  
- **Wind:** 6 to 12 mph S  
- **Forecast:** Mostly clear.  

### Friday:  
- **Temperature:** 70°F (falling to 66°F in the afternoon)  
- **Wind:** 5 to 14 mph S  
- **Forecast:** Partly sunny.  

Let me know if you'd like more details!

Here's the current weather forecast for New York:

### Today:  
- **Temperature:** 73°F  
- **Wind:** 7 mph NW  
- **Forecast:** Mostly sunny, with a high near 73.  

### Tonight:  
- **Temperature:** 57°F  
- **Wind:** 3 to 7 mph SE  
- **Forecast:** Mostly clear.  

### Thursday:  
- **Temperature:** 68°F (falling to 64°F in the afternoon)  
- **Wind:** 3 to 12 mph SE  
- **Forecast:** Sunny.  

### Thursday Night:  
- **Temperature:** 56°F  
- **Wind:** 6 to 12 mph S  
- **Forecast:** Mostly clear.  

### Friday:  
- **Temperature:** 70°F (falling to 66°F in the afternoon)  
- **Wind:** 5 to 14 mph S  
- **Forecast:** Partly sunny.  

Let me know if you'd like more details!

Query: 

```

## Golang版

> https://github.com/guobinqiu/mcp-demo-golang

