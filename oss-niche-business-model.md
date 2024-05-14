# Business Model for Niche Open Source Software

Came up in the context of thinking about sports team management apps, when I made the remark that the reason they're universally terrible is because everyone is putting making money over actually making something users enjoy using. There's not a huge amount of money in volunteer team sports, so advertising-funded free-to-play seems to be the business plan they've all settled. Hence the lack of both good UX and not using well-known standards that could make it easier for people to fit these apps into the rest of their life, eg ics.

They're a dime a dozen, but they're universally terrible. So the solution is of course yet another one... but how to fund it so it doesn't end up just another one in the cesspool. 

Well, open source would be ideal to get a team to work on it, but there's not too many OSS developers who this would appeal to. So this requires a business model to provide an incentive! Not dependent on outside capital in the beginning, only volunteer development.

What are the goals and what is the timeline, and how could it be funded from the get-go. Need to pay overheads (hosting, dev $ accounts, etc) and then the remainder should go to the developers.The former is relatively straightforward to work out, but the latter is tricky.

Principles:

- Payment should be proportional to work invested
- Not looking for anyone to get filthy rich, just a decent payrate.
- Pay should based off revenue in the future (it depends on work done now!)

So this is a concept for implementation, probably ridiculously flawed in some way.

- determine features for MVP: v1.0, defer others to 2.0+
- come up with a remuneration token, call it devBucks (cannot use -coin, ha!) and dB as abbreviation is hilarious to me.
- allocate 100dB or 1000dB to v1.0
- split dB allocation between features
- devs get a dB account.

- dB recompense for lowering overheads too, ie 50% as dB
- to handle the situation where devs contribute once, then not again
    - originally I thought 1-3 years to get paid from revenue for work done, but instead
    - dB has deflation built in... rate can be tweaked over time, but start with 50%
    - so work pays ~100% dB first year, ~50% 2nd, ~25% 3rd... but do it with continuous/exponential
    - perhaps not until revenue starts and a minimum payment received... then backoff starts


# Sports Team Management App

# MVP v1.0

- CRM: clubs, teams, team members, coaches, support, admins
    - privacy dependent on membership of a team... initially only message from app
    - clubs visible to all? option at start
- Events: games, training time, meetings
    - mark attendance
- Communications
    - last minute
    - regular updates

## Implementation notes
- Communications
    - notifications: email, SMS, WhatsApp bot, FB messenger, phone

- Web only, but can be put on home screen?
- maybe? 'native app' could be basic wrapper to allow for Apple/Google notifications

## v2.0+:

- integration with native apps (add to calendar, contacts) is v2.0
- social media integration... write update in app
- but easy post to Insta, FB, WhatsApp