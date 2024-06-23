css ='''
<style>

.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
}
.chat-message.bot {
    background: #f3f3f3;
    border: 1px solid #d9d9d9;
    color: #242424;
}
.chat-message.user {
    background: #318CE7;
    border: 1px solid #d9d9d9;
    color: white;
}
.chat-message .avatar {
    width: 30px;
    height: 30px;
}

.chat-message .message {
    color: #242424;
    background: #F3F3F3;
    padding: 10px;
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.4;
    max-width: 100%;
    word-wrap: break-word;
    display: inline-block;
}

.chat-message .avatar img {
    border-radius: 50%;
    width: 30px;
    height: 30px;
}
.user {
    animation: come 0.3s ease-in;
}
</style>
'''

bot_template ='''
<div class="chat-message bot">
<div class="avatar">
    <img src="https://i.ibb.co/qWBwpNb/Photo-logo-5.png" style="max-height:78px; max-width:78px; border-radius:50%;">
</div>
  <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png" style="max-height:78px; max-width:78px; border-radius:50%;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

