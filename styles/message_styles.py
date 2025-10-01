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


