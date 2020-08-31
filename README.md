# hackler
> 
> A Discord bot by ChaseLP

> (Gets bot's private key from file ".env" in the directory)
> 
> \# .env
> 
> DISCORD_TOKEN=[private key]

> In addition to commands, bot responds to "hello" and says jokes when triggered by keywords

### Current features:
- !parse [mathexpr]
> *converts math expression to infix notation, supports + - \* / %*
- !solve [mathexpr]
> *converts to infix notation then solves math expression, supports + - \* / %*
- !make public channel [name]
> *creates a public channel for the user*
- !make channel [name]
> *same as make public channel*
- !make private channel [name]
> *creates a private channel for the user and a role for this channel to read/write*
- !delete channel [name]
> *deletes the channel, must have been created by the requesting user*
- !allow [otheruser] [channelname]
> *adds other user to role of private channel to allow read/write*
- !revoke [otheruser] [channelname]
> *removes other user from role of private channel, disallowing read/write*
