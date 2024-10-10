# Lab1 : Chat Application

Github Repository Link: https://github.com/tvp590/Ense-472-Digital-Networks/tree/main/Lab1

Team Members:
- Tirth V Patel : 200435378
- Ramanpreet singh : 200384219


## Lab Overview

This lab  implements a real-time chat application that allows users to communicate seamlessly.

### Phase Overview

#### Phase 1: Echo Service
- Developed a server that collects any message sent to it and returns the same message back to the client.
- Implemented client-side functionality to display received messages, enhancing user interaction.

#### Phase 2: Chat service
- Modified the server to broadcast messages from one client to all other connected clients.
- Each message sent now contains identifying information, such as the client’s address and port number, to clarify the sender.

#### Phase 3: Better Chat
- Implemented a feature that prompts clients to choose a username upon connecting, replacing IP addresses in chat displays.
- System notified all clients when a new user joined or left the chat.