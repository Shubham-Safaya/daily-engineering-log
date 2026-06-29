<!-- Ready for Medium. Published 2026-06-29. Part of 'The Identity Layer' by Shubham Safaya. No em dashes. -->

# The Graph Underneath

People imagine a customer profile as a tidy card. A name at the top, an email, a phone number, a neat list of purchases. That picture is comforting and almost entirely wrong. What actually sits under a resolved customer is a messy network, and learning to see it as a network is the moment identity resolution starts to make sense.

In the real structure, the nodes are not people. The nodes are identifiers. An email is a node. A phone number is a node. A device ID, a loyalty number, a hashed login, a shipping address. Each of these is a separate point in the graph. The people are not stored anywhere as a single object. A person is something the system infers by deciding which identifiers belong together.

The edges are evidence. A login event ties an email to a device. A purchase ties a loyalty card to a payment token. A shipping label ties a name to an address. Every edge has a strength, because some evidence is strong and some is weak. A login is strong. Two people who happen to share a couch and a wifi network is weak.

Resolution, in this picture, is graph clustering. You find the connected groups of identifiers, you score the edges that hold them together, and you cut the edges that are too weak to trust. What is left, each surviving cluster, is your best guess at one human being. Change the threshold for cutting and you change how many people you think you have.

## The hard problems are policies, not algorithms

Once you see identity as a graph, the clustering algorithm stops being the interesting part. You can implement connected components in an afternoon. The questions that actually consume teams are policy questions, and there are four that come up every single time.

Survivorship is the first. When two records merge and they disagree, which value wins? One says the customer lives in Texas, the other says Oregon. One spells the name with an i, the other with a y. Somebody has to decide the rule for which truth survives the merge, and that rule has real consequences for everything from shipping to personalization.

Decay is the second. Evidence gets old. That phone number from a few years ago, the one nobody has used since, how long should it keep holding two identifiers together? Treat old evidence as fresh and you merge people who have moved on from each other. Discard it too quickly and you fracture real people into pieces.

Households are the third, and they are genuinely hard. Two people, one address, one shared account, one streaming login used by the whole family. Is that one node or two? The right answer depends entirely on what you are about to do. For shipping, the household is the unit. For personalization, the individual is the unit, and confusing the two is how a parent ends up seeing recommendations meant for their teenager.

Deletion is the fourth, and it is the one that turns identity from a marketing tool into a compliance obligation. A privacy request arrives. Which edges have to die? What happens to the cluster when you remove an identifier that was holding it together? Does the rest of the profile survive, and can you prove that the deleted identifier is truly gone from every downstream copy? If your graph cannot answer this cleanly, you do not have an asset. You have an audit waiting to happen.

## Why the network view changes how you build

The reason this matters beyond being a nice mental model is that it changes what you measure and what you protect. If you think of profiles as cards, you protect cards. If you think of identity as a graph of evidence, you start protecting the edges. You version them. You log when each one was created and from what event. You build the ability to remove a single edge and recompute the affected clusters without rebuilding the whole world.

The graph view also makes the privacy story tractable. Deletion stops being a frightening, vaguely defined obligation and becomes a concrete operation: find the nodes for this person, remove them and their edges, recluster the neighborhood, certify the result. That is a thing you can build, monitor, and prove.

The algorithm is a weekend project. The policies around survivorship, decay, households, and deletion are the actual work, and they are the difference between an identity system you can defend and one you are quietly hoping nobody asks too many questions about.


---

*This essay is part of an ongoing series, [The Identity Layer](https://github.com/Shubham-Safaya/daily-engineering-log/tree/main/book), where I work out in public how customer identity, advertising, and privacy fit together. I am a Senior Product Manager at Walmart Global Tech. Follow on [LinkedIn](https://www.linkedin.com/in/shubham-safaya/).*
