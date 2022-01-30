# iQuHack2022

# spiNYpizza

## A quantum secure chat among N users
Just some nice dudes and a lady, 4 italians spread around the world and one NY guy

<img src=“logo.png” width=“250">
                               
So we are:
- Lisa Bombieri
- Andrea Maiani
- Leonardo Placidi
- Ciro Gus Salcedo
- Alessandro Summer
# Authentication scheme
## Network topology
Nodes of the network
- S: Messaging server
- I: Interface (authentication server)
- U1, U2, U3, ... : Users
<img src=“sketch.png” width=“250">
## Authentication protocol
The point of the authentication protocol is to establish a series of *secure links* between the server (S) and
each user (U_i). For each user, the messaging server (S) plays the role of Alice and the user (U_i) plays the role
of Bob. They interact with direct messages to the interface server (I).
In this way, the basis are shared _only_ between Alice, Bob and the Interface.
The authentication algorithm is as follows:
FOR EACH USER U_i:
1. S sends MESSAGE_i to I
2. S sends A_BASIS_i to I
3. U_i sends B_BASIS_i to I
4. I execute BB84
5. I sends RESULTS_i to U_i
6.  U_i sends B_BASIS_i to S
7.  S sends A_BASIS_i to U_i
8.  U_i eliminates bits with wrong basis from RESULTS_i : U_i has key K_i
9.  U_i sends index of bits to be eliminated to S
10. S eliminates the bits : S has key K_i


<img src=“key.png” width=“500">
                              
## Implementation
- a main server used to communicate between different users classically
- the ‘quantum servers’ are used to communicate only with the Intermediate interface
- The intermediate interface communicate with the Quantum Computer assembling a circuit that implements Ekert91 or BB84 depending on the input received by a couple of users
- The basis used for the qkd protocol are then shared between the users passing through the main server (S)
## The actual example
- Two users communicate with a main server classically
- When one of the two write the command ‘/BASIS’
- - A protocol between the E91 and BB84 is chose
- - Alice generates automatically her basis and the bitstring (in the case the BB84 is selected)
- - Bob generates automatically his basis
- - Both the txt files are sent to the private servers that communicates them to the intermediate interface
- - The intermediate interface assemble the circuit and run it on the QuTech computer
- - Two output are created and sent back to the two users
- - Comparing the basis using the main server the quantum-key is selected
- The communication between the two users is now quantic secure using the quantum-key to encrypt and decrypt the files privately
                              
<img src=“actual_nw.png” width=“500">

## Team Experiences
We chose to work on the Quantum Key Distribution challenge. We split up into two groups: one working on the classical end and another on the quantum. On the classical end, we had a task brand new to all of us, network programming. We decided to implement our system as a chatroom where the two users could talk to each other classically and each user had a personal server for sending quantum information to the quantum computer. We underestimated the complexity of this task as the network code was difficult to produce in the first place, given our experience. The challenge ended around when we were working on integrating the classical and quantum system. On the quantum end, we replicated the BB84 and E91 algorithm and developed a format from sending classical instructions from the users to the quantum interface.
