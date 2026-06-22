<!-- Ready for Medium. Published 2026-06-22. Part of 'The Identity Layer' by Shubham Safaya. No em dashes. -->

# Deterministic and Probabilistic, and the Space Between

There are two ways to decide that two records belong to the same person, and almost every real system is a negotiation between them.

Deterministic matching says the hashed emails are identical, therefore it is the same person. This is hard evidence. The confidence is close to certainty. The catch is coverage. Plenty of records do not share a clean identifier, so deterministic matching alone leaves a lot of the same people looking like strangers.

Probabilistic matching says the last names are the same, the zip codes match, the devices behave alike, and the timing lines up, therefore it is probably the same person, with some confidence below certainty. This is soft evidence. It covers the cases deterministic matching cannot reach, and it pays for that coverage with a risk of being wrong.

The mistake people make is treating this as a contest with a winner. It is not. Different businesses live at different points on the line between the two, and they live there for good reasons.

## The cost of being wrong points in two directions

A bank leans deterministic because a false merge is a catastrophe. Linking two customers who are not the same person can expose one person's account to another. The cost of a wrong merge is so high that the bank would rather miss real matches than risk a single false one.

An advertising platform leans probabilistic because a missed match is just a wasted impression. If the system fails to recognize that a phone and a laptop belong to the same person, the worst case is showing one extra ad. The cost of a miss is small, so the platform happily accepts more guessing in exchange for more reach.

Retail sits in the uncomfortable middle, and that is what makes it interesting. Loyalty data is deterministic gold, because the customer identified themselves at the register. Guest checkout is probabilistic fog, because the customer told you almost nothing. The same company holds both, and it has to serve use cases at both ends of the risk spectrum from one identity graph.

## One graph, many thresholds

The resolution I have landed on, after building these systems at scale, is that you do not pick one confidence threshold. You build one identity graph that records the strength of every link, and then you let each consumer of the graph choose the threshold that fits its tolerance for being wrong.

The marketing team activating a broad awareness campaign can accept links at lower confidence. A missed person costs them a fraction of a cent, and a wrong person costs them only slightly more. Let them reach wide.

The team making decisions that touch money or sensitive categories should demand high confidence. For them, a wrong link is a real harm to a real person, and they should accept duplicates and misses rather than risk a false merge.

This reframing matters because it turns a religious argument into a product decision. Instead of the deterministic camp and the probabilistic camp fighting over which is correct, you give every team a dial and you make them own where they set it. The graph carries the evidence. The threshold carries the judgment. And the judgment is different for advertising than it is for finance, which is exactly as it should be.

The algorithm underneath all of this is genuinely simple. The hard part, the part that takes quarters and a privacy lawyer in the room, is deciding how confident you need to be before you are willing to say that two records are one human being. That is not an engineering question. It is a question about what it costs you to be wrong, and which direction you would rather be wrong in.


---

*This essay is part of an ongoing series, [The Identity Layer](https://github.com/Shubham-Safaya/daily-engineering-log/tree/main/book), where I work out in public how customer identity, advertising, and privacy fit together. I am a Senior Product Manager at Walmart Global Tech. Follow on [LinkedIn](https://www.linkedin.com/in/shubham-safaya/).*
