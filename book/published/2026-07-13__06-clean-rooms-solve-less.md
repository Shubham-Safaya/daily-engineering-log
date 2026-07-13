<!-- Ready for Medium. Published 2026-07-13. Part of 'The Identity Layer' by Shubham Safaya. No em dashes. -->

# Clean Rooms Solve Less Than You Think

The clean room is the most oversold idea in modern advertising, and I say that as someone who builds with them and believes in them. The pitch is irresistible. Two companies collaborate on data without either side seeing the other's raw records. Match, query, measure, all without exposing a single email. It sounds like the answer to every privacy question anyone has ever asked.

It is not the answer to those questions. It is a secure calculator, and a secure calculator cannot fix a disagreement about what you are calculating.

Here is the failure I have watched play out more than once. Brand A has purchase data. Retailer B has loyalty data. They both want to know whether a campaign drove sales. They load their data into a clean room, run the overlap, and get a thirty four percent match. Both sides conclude the clean room does not work, and the project quietly dies.

The clean room worked perfectly. The definitions were broken, and no amount of cryptography can repair a broken definition.

## The boring meetings have to come first

When you take apart that thirty four percent, the technology is never the culprit. The culprit is always a set of unexamined assumptions that the two parties never reconciled before they started.

One side defined a customer as anyone who purchased in the last twelve months. The other defined a customer as anyone who has ever held a loyalty card. Those two populations were never going to fully overlap, because they are answers to different questions.

One side normalized emails before hashing, lowercasing them and stripping the dots and the plus tags. The other hashed the raw string exactly as the customer typed it. The same person produced two different hashes, and two different hashes never match, no matter how good the clean room is.

One side loaded ninety days of data. The other loaded a full year. The overlap looked thin not because the customers differed but because the time windows did.

One side was measuring individual people. The other was measuring households. The grain did not line up, so the counts could not either.

Every one of these is a definition problem, and every one of them is invisible inside the clean room. The room faithfully computes the overlap of whatever you give it. If what you give it disagrees about what a customer is, how identifiers are formatted, what window you are looking at, and whether you are counting people or households, the room will hand you a small number and you will blame the room.

## What to settle before you load a single row

The discipline that makes clean rooms actually deliver is unglamorous and entirely upstream. Before anyone loads data, the two parties have to agree, in writing, on four things.

What is a customer, in a definition both sides will use. What identifiers are we matching on, normalized in exactly the same way, hashed with exactly the same recipe. What lookback window are we both committing to. And what is the grain of the output, person or household or campaign, so the numbers mean the same thing on both sides.

These are not technical decisions. They are negotiated agreements between two organizations that usually have never compared their data definitions before. The meetings are tedious. They involve people from legal and analytics and engineering on both sides arguing about what should be a trivial question and turns out not to be. And those tedious meetings are the entire difference between a clean room that produces a credible number and one that produces a thirty four percent that ends the project.

The clean room is real and useful. It genuinely lets parties collaborate without exposing raw data, and that is a meaningful privacy advance. But it solves the second problem, the secure computation problem. It does nothing for the first problem, the agreement problem, and the first problem is the one that kills most projects. Buy the calculator if you like. Just do not expect it to do the arithmetic of deciding what you are counting. That part is still yours.


---

*This essay is part of an ongoing series, [The Identity Layer](https://github.com/Shubham-Safaya/daily-engineering-log/tree/main/book), where I work out in public how customer identity, advertising, and privacy fit together. I am a Senior Product Manager at Walmart Global Tech. Follow on [LinkedIn](https://www.linkedin.com/in/shubham-safaya/).*
