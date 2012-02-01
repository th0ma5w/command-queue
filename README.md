# command queue!

## What is this?

This is a minimalistic set of scripts that implement a client and server for the purposes of queueing shell commands. 

## How does it work?

The client connects to the server and submits a parameter to be queued by the server. Multiple clients can contact the server at the same time, although the network stack and the GIL may actually force one-at-a-time execution. The server then keeps an internal list and slowly executes the command it is configured with paired with the parameters that have been queued by clients.

## Why would I need this?

In some distributed computing situations, some components are not always hardend to allow multiple actors executing the command at nearly the same time. This can force those requests to ultimately be executed one-at-a-time.

## What are the requirements?

Any Python compatible install that is compatible with the Python libraries used (which are mostly a part of the default library) since version 2.6. This may include Jython or PyPy but has not been tested with either of those, nor has it been tested with Python 3.0.

## How do I make it work?

1. Download the code, and configure the server with the command that will be executed for each parameter that is submitted. Currently the command is to just "echo" the parameters that have been submitted.

2. Start the server, and leave it running.

3. Run the submission script with a parameter, and observe the server script queue, and then execute each submission.

## Why did you write this and why is it on GitHub?

Good question! I wrote it as a proof-of-concept at my job, and it turns out that this concept is actually implemented in some of our other tools, so this wasn't needed. Hopefully you can find some use for it, let me know, or at least if you are learning Python you can take a look at some of the things that it does.

## Support?

Write me note on here, but otherwise, I am not responsible for any of it, and you use it at your own risk, and I make no claims as to its suitability for any task.
