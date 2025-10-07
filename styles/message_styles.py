def style_message(text, role):
    if role == "user":
        return f"""
        <div style="
            background-color: #013220;
            color:white;
            padding: 10px;
            margin: 5px 10px 5px 300px;
            border-radius: 10px;
            text-align: left;
        ">
            {"You: "+text}
            
        </div>
        """
    else:
        return f"""
        <div style="
            background-color: #575757;
            color:white;
            padding: 10px;
            margin: 5px 150px 5px 10px;
            border-radius: 10px;
            text-align: left;
        ">
            {"  Bot: "+text}
            
        </div>
        """

# styles/message_styles.py

def chat_container_css():
    return """
    <style>
    .chat-container {
        height: 70vh;
        overflow-y: auto;
        padding-bottom: 80px; /* space for input box */
    }
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 10px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    </style>
    """

