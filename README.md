# Alpha Bot - A Multi Purpose Chat App 🔥

<p align="center">
  <img src="img/alpha-bot.png" alt="Chat App with Textbase UI" style="width: 200px; height: 200px;">
</p>

## Introduction 🚀

This is a chat application that has been built upon the UI of Textbase [✨ Textbase is a framework for building chatbots using NLP and ML. ✨], a powerful and flexible UI framework for creating chat interfaces. The app integrates various APIs to provide additional functionalities like URL shortening, text translation, holiday information, internet queries, and meme generation.


## Installation 📥

1. Clone the Textbase repository: 

```bash
git clone https://github.com/cofactoryai/textbase.git
```

2. Clone this Chat App repository: 

```bash
git clone https://github.com/your-username/chat-app.git
```

3. Copy the contents of the "chat-app" repository into the "textbase" repository.

4. Navigate to the "textbase" directory: 

```bash
cd textbase
```

5. Start the server to run the Chat App: 

```bash
python server.py
```

6. Open your web browser and go to `http://localhost:5000` to access the Chat App.

## Features 🌟

The Chat App extends the capabilities of the Textbase UI with the following API integrations:

- `urlshorten [Link]`: To get a shortened link for your long URL.
- `translate [Text]`: To translate your text from English to Hindi.
- `holidays`: To fetch all the public holidays of your country.
- `ask [Query]`: To ask any query from the internet.
- `meme`: To generate a meme.

## Usage 📝

1. Type your message in the text input at the bottom of the Chat App.
2. To use any of the integrated APIs, type the corresponding command followed by the required parameters (if any).
3. Press "Enter" or click the "Send" button to submit your message and view the response.

**Examples:**

- To get a shortened link: 💡
  ```
  urlshorten https://www.example.com
  ```

- To translate text: 🔤
  ```
  translate Hello, how are you?
  ```

- To fetch holidays: 🏖️
  ```
  holidays
  ```

- To ask a query: ❓
  ```
  ask What is the capital of France?
  ```

- To generate a meme: 🎭
  ```
  meme
  ```

## Contribution 🤝

Contributions to the Chat App with Textbase UI are welcome! If you have any feature suggestions, bug reports, or improvements, feel free to create a pull request or open an issue on the repository.

## License 📜

This Chat App with Textbase UI is licensed under the [MIT License](LICENSE).

## Acknowledgments 👏

- The Textbase UI framework by CofactoryAI (https://github.com/cofactoryai/textbase) for providing the foundation for this chat application.
- The developers of the various APIs used in this app for their invaluable services.
