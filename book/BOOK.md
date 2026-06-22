# The Identity Layer
### How customer identity, advertising, and privacy actually fit together

*A book assembling itself in public, one weekly essay at a time, by Shubham Safaya.*

*Manuscript regenerated 2026-06-22 18:00 UTC.*

---

## Table of contents

1. Who Is the Customer, Really?
2. Match Rates Lie
3. Deterministic and Probabilistic, and the Space Between
4. The Graph Underneath
5. The Cookie Died, Identity Did Not
6. Clean Rooms Solve Less Than You Think
7. Privacy Is Not a Feature, It Is the Foundation
8. Retail Media Is an Identity Business Wearing an Ads Costume

---


## Chapter 1

## Who Is the Customer, Really?

Every company I have ever worked with claims to be customer obsessed. Very few of them can answer a simpler question: who, in the data, is the customer?

Not in the marketing-deck sense. In the literal, technical sense. When a person shops on your app on Monday, visits your website from a work laptop on Tuesday, walks into a store and pays cash on Wednesday, and clicks an email on Thursday, your systems see four events. Are those four events one person or four? The honest answer at most companies is that nobody knows, and the systems quietly disagree with each other about it.

This is the problem identity resolution exists to solve, and it is the foundation that everything else in modern advertising, personalization, and customer experience is built on. Get it wrong in one direction and you treat one person as four, mailing them the same coupon four times and counting them as four customers in your board deck. Get it wrong in the other direction and you merge two different people into one profile, so now your personalization engine is recommending baby formula to a college student because it confused them with a young parent who shares a last name and a zip code.

## The definition problem comes before the technology problem

When teams set out to fix identity, they almost always start by buying a tool. A customer data platform, a clean room, an identity vendor. This is backwards. The first artifact you need is not software. It is a written definition of what a customer is.

I have watched a single company hold three contradictory definitions at once. The loyalty team counted a customer as anyone with a rewards card. The ecommerce team counted a customer as anyone who placed an order in the last twelve months. The advertising team counted a customer as any device that had seen an ad. None of these are wrong. They are answers to different questions. The trouble starts when you try to join them and the numbers refuse to agree, and everyone blames the data instead of the definitions.

So before any vendor evaluation, I push teams to answer five questions in writing.

What is the atomic unit: a person, a household, a device, or an account? A household of four sharing one streaming login is one account but four people. A person with two phones is one person but two devices. Your unit changes every number downstream.

What identifiers do we trust, and in what order? Email, phone, loyalty ID, device ID, address. Some are stable and some rot. Some are deterministic and some are guesses.

What is our tolerance for a false merge versus a missed match, and does that tolerance change by use case? Advertising can live with mistakes that finance cannot.

How fresh does identity need to be? A profile that updates monthly is fine for a quarterly business review and useless for a real-time website experience.

And finally, when a person asks to be forgotten, what exactly do we delete, and how do we prove it? If you cannot answer this one, you do not have an identity system. You have a liability.

## Why this is a product problem, not an engineering problem

The reason identity resolution belongs to product and not only to engineering is that almost every hard question is a tradeoff between business outcomes, not a question with a single correct technical answer.

The matching algorithm is the easy part. You can stand up deterministic matching on hashed emails in an afternoon and add fuzzy name matching in a week. What takes quarters is deciding the policies. Which address wins when two records disagree. How long a phone number counts as evidence after it goes silent. Whether two people at one address are one node or two. What happens to a merged profile when one of the merged identifiers is deleted. These are judgment calls with money and risk and customer trust on both sides, and that is exactly the kind of decision a product manager exists to own.

I have come to believe that the quality of a company's identity layer is the ceiling on the quality of everything customer facing it can ever do. You cannot personalize for a person you cannot recognize. You cannot measure the effect of an ad on a customer you cannot follow from impression to purchase. You cannot honor a privacy request for a person whose records you cannot find. Recognition comes first. Everything else is built on top of it.

So the next time someone says their company is customer obsessed, ask them the plain question. Who is the customer, in the data? If they have a crisp answer, they are further along than most. If they pause, you have just found the most important unsolved problem in their business, and probably the most valuable one.

---


## Chapter 2

## Match Rates Lie

A vendor once told me their match rate was ninety percent. My own measurement said sixty. Neither of us was lying. We were dividing by different numbers, and the gap between us was the entire story of how identity gets oversold.

A match rate is a fraction. Matches on top, some population on the bottom. The number you get depends almost entirely on what you choose to put on the bottom, and the industry has quietly agreed to choose flattering denominators.

If a vendor matches against only the records that already have a clean, valid, hashed email, they have thrown away the hard cases before they started counting. Of course the rate looks heroic. They are grading themselves on the questions they already knew the answers to. The records without good identifiers, the ones that actually needed resolving, never made it into the denominator.

## The four questions that deflate any match rate

After enough of these conversations, I built a short list of questions that I now ask every data partner before I trust a single percentage.

What is the denominator? Matches over all records, or matches over only the records that were already easy to match? This one question alone usually explains the gap between two numbers.

At what grain did you match? Person, household, or device? A household match counts a husband and wife as one success. A device match counts the same person's phone and laptop as two. The grain quietly changes the number by ten or twenty points and nobody mentions it unless you ask.

What is the false positive rate, not just the match rate? This is the question vendors least want to answer. A high match rate with a high false positive rate is worse than a modest honest one, because every false positive is a real person wrongly merged with a stranger. You will pay for those mistakes later in customer complaints and in personalization that feels broken.

How fresh was the truth set you matched against? If you are matching today's customers against an identity graph last refreshed a year ago, your misses are not all real misses. Some are people who simply moved or changed their email since the graph was built.

## Why the honest number is the useful one

There is a temptation, when you finally get a vendor to admit the real number, to be disappointed. Sixty percent sounds so much worse than ninety. But the honest sixty is worth more than the inflated ninety, because you can actually make decisions with it.

When I tightened how we measured matching at scale, the headline number went down and the quality of every downstream decision went up. We stopped congratulating ourselves on matches that were really false positives. We found the segments where matching genuinely failed and fixed the upstream data instead of papering over it. The lower number told the truth, and the truth is what you build on.

There is a deeper lesson here that goes beyond identity. Any metric that a vendor controls the definition of is a metric you should distrust until you can recompute it yourself. Match rate, viewability, attribution, addressability. Each of these has a flattering definition and an honest one, and the flattering definition is always the one in the sales deck. The job of a serious product manager is to insist on the honest one, even when the honest one is the one that makes your own program look less impressive this quarter.

Trust the methodology, not the percentage. When someone leads with a number instead of a method, the number is doing the work that the method could not.

---


## Chapter 3

## Deterministic and Probabilistic, and the Space Between

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


## Chapter 4

## The Graph Underneath

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


## Chapter 5

## The Cookie Died, Identity Did Not

For years the third party cookie was the quiet scaffolding under most of digital advertising. When it finally crumbled, a lot of people expected the building to come down with it. The strange and instructive thing is how little actually did, and what the rubble revealed about where value really lived all along.

The third party cookie let advertisers follow people across websites they did not own. That was its whole magic and its whole problem. It was powerful because it tracked strangers across the open web. It was doomed because tracking strangers across the open web is exactly what regulators, browser makers, and ordinary people decided they no longer wanted.

When it went away, four things rushed in to replace it, and the pattern across all four is the same.

First party data became the new foundation. Loyalty programs, logins, purchase histories. The data a company collects from its own customers, with a direct relationship behind it. Companies that had treated their first party data as exhaust suddenly realized they were sitting on the scarcest asset in advertising.

Hashed identifiers became the connective tissue. Email and phone, normalized and hashed, matched privately between parties without exposing the raw values. Not as universal as the cookie, but built on a real relationship rather than covert tracking.

Clean rooms became the meeting place. Instead of shipping data around, two parties bring their data into a controlled environment, match on shared identifiers, and walk away with aggregate answers without either side seeing the other's raw records.

Modeled audiences filled the gaps. Where direct signal is thin, you use probabilistic models to estimate who is likely similar to your known customers. A stand in for the certainty the cookie used to fake.

## The value moved, it did not vanish

Notice the through line. Every replacement is grounded in something the cookie never required: an actual relationship with an actual customer, and the ability to prove things about that relationship without leaking it. The center of gravity moved from tracking people across the web to knowing your own customers deeply and being able to use that knowledge safely.

This is the real reason retail media exploded at exactly the moment the cookie faded. Retailers always held the best first party signal in commerce, which is what people actually bought. While the cookie was alive, that signal was just one input among many and not an especially glamorous one. When the cookie died and first party purchase data became the scarcest thing in the market, retailers discovered they had been sitting on the new oil the entire time.

## The uncomfortable question this leaves on the table

If the post cookie world rewards companies that know their own customers and can prove it, then the urgent question for any business is no longer how do we track people across the internet. It is whether your own first party data is actually organized well enough to be an asset at all.

Most companies, asked this directly, will say yes and mean no. They have the data, technically. It is scattered across a dozen systems that disagree about who the customer is, stored under definitions that were never reconciled, with identity links that nobody has audited and consent state that lives somewhere else entirely. Having the data and being able to use it as a coherent asset are completely different things, and the gap between them is precisely the identity work this book is about.

The cookie did not make identity harder. It had been letting companies avoid the harder, more honest work of knowing their own customers. Its death just sent everyone back to the homework they had been putting off. The companies that do that homework will own the next decade of customer relationships. The ones that keep hoping for a cookie replacement that requires no real relationship are waiting for a thing that is not coming.

---


## Chapter 6

## Clean Rooms Solve Less Than You Think

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


## Chapter 7

## Privacy Is Not a Feature, It Is the Foundation

I have watched privacy handled two ways, and the difference between them decides whether a data organization moves fast or moves scared.

The first way treats privacy as a review gate. The team designs the product, builds it, and then sends it to legal near the end to get blessed. In this world privacy is a blocker by definition. It arrives late, it says no, deadlines slip, and everyone learns to resent the people whose job is to protect the company and its customers. The incentives are set up so that the privacy team and the product team are on opposite sides of the table, which is exactly backwards.

The second way treats privacy as a property of the system, designed in from the first diagram. The data flow is built so that the privacy answer is yes by construction. Sensitive fields never enter the pipeline in the first place. Deletion runs automatically rather than as a manual scramble. An opt out propagates to every downstream system without a human carrying it there by hand. In this world privacy is not a gate you pass through at the end. It is a constraint you designed around at the beginning, the way you design around a performance budget or an uptime target.

The second way is faster. That is the part people find counterintuitive. Surely all that privacy engineering slows you down. In practice the reviews get faster because there is less to review. When sensitive data never entered the system, there is no anxious conversation about what to do with it. When deletion is automated and monitored, a privacy request is a routine event with an SLA, not a fire drill. Designing privacy in does not tax your speed. It is what lets you keep your speed as the data and the regulations grow.

## A deletion request is a feature, not an interruption

The reframe that unlocked this for me is simple. A deletion request is not an interruption to your data platform. It is a feature of your data platform.

Think about how you treat search, or checkout, or any core capability. It has an owner. It has monitoring. It has a service level it is expected to meet. It has tests that fail loudly when it breaks. Now ask whether the right to be forgotten has any of those things in most organizations. Usually it has none of them. It is handled by a person running a query when a request comes in, with no monitoring, no SLA, and no proof that the deletion actually reached every copy of the data.

Treat it instead like the feature it legally and morally is. Give it an owner. Give it monitoring that alerts when deletions fail or lag. Give it an SLA you actually measure against. Build the certification that proves an identifier is gone from every downstream system, not just the one the request happened to land in. The moment you do this, the entire posture of the organization changes. Privacy stops being the thing that slows you down and becomes a capability you can point to with confidence when a partner or a regulator asks.

## Trust travels, and that is a business advantage

There is a competitive edge hiding in all of this that rarely gets named. Companies that build privacy into the foundation sign data partnerships faster, because trust travels. When a potential partner does diligence and finds that your deletion is automated, your consent state propagates cleanly, and your sensitive data handling is provable, they say yes sooner and with fewer conditions. When they find a manual, hopeful, undocumented process, they slow down, they add contractual protections, and sometimes they walk away.

Processing tens of millions of new records under a privacy by design model, the thing I noticed was not that privacy made us cautious. It made us credible. We could enter conversations that more cavalier competitors could not finish, because we could show our work.

So the question to ask about your own organization is a structural one. Is privacy upstream or downstream of your product decisions? If it sits downstream, as a review you pass at the end, you will always experience it as friction. If it sits upstream, as a constraint you design around from the start, it becomes the foundation that lets you build everything else with confidence. Privacy is not the tax you pay for handling customer data. It is the foundation that makes handling customer data a durable business at all.

---


## Chapter 8

## Retail Media Is an Identity Business Wearing an Ads Costume

Retail media is the fastest growing channel in advertising, and it is almost always explained as an advertising story. Retailers have screens and shelves and checkout pages, brands want to reach shoppers, so retailers sell access to their audience and book high margin revenue. That story is true, and it misses the actual engine entirely.

Underneath the advertising costume, retail media is an identity business. The ad inventory is the storefront. The identity layer is the inventory that matters, and the networks that win are the ones whose identity layer is the most accurate, the most compliant, and the most provable to a skeptical buyer.

Consider why a brand pays a retailer at all. It is not for the ad slots. Ad slots are everywhere and mostly cheap. The brand pays for one thing the retailer can offer that almost nobody else can: proof of who actually bought. Not who clicked, not who hovered, not who was probably interested. Who walked out with the product. Purchase data is the closest thing in commerce to ground truth, and the retailer is one of the few parties that holds it.

But holding purchase data is not the same as being able to use it. To turn that data into a retail media business, the retailer has to do three things, and all three are identity problems.

## Three identity problems in an advertising trench coat

First, the retailer has to match the brand's audience to its own real shoppers. The brand says it wants to reach lapsed buyers of its category, or new parents, or people who buy premium. Connecting that intent to actual identified shoppers in the retailer's base is identity resolution, full stop. If the matching is sloppy, the targeting is sloppy, and the brand is paying for reach it is not really getting.

Second, the retailer has to target without leaking personal data. The brand cannot see the retailer's customer list, and the retailer cannot expose it. The whole activation has to happen across a privacy boundary, through hashed identifiers and clean rooms and consent aware pipelines. This is privacy engineering, and it is load bearing. Get it wrong and you do not have a growth channel, you have a regulatory incident.

Third, and this is where the money is proven, the retailer has to close the loop. It has to connect the ad a person saw to the purchase that person made, often on a different device or days later or in a physical store. That connection, impression to receipt, is identity again. Without resolving the viewer of the ad to the buyer of the product, you cannot prove the campaign worked, and a campaign you cannot prove is a campaign that loses its budget the moment a CFO starts asking questions.

## The moat is the graph, not the inventory

Once you see retail media this way, the competitive picture rearranges itself. The networks people assume are winning because they have the most ad placements are not necessarily winning at all. The ones that will last are the ones with the best identity layer: the most accurate matching, the cleanest privacy posture, and the most credible closed loop measurement.

This is also why so many retail media networks look impressive in the sales deck and disappoint in the results. The deck sells inventory. The results depend on identity. A network can have beautiful ad units and a huge audience and still deliver mushy outcomes, because its identity layer cannot match cleanly, cannot measure honestly, and cannot prove incrementality to a buyer who has learned to ask hard questions.

So when someone asks me which retail media network is best, I do not ask about their ad formats or their audience size. I ask whose identity layer I would trust to tell me the truth about whether my money worked. That is the real product. The media is the storefront out front. The identity graph is the inventory in the back, and the inventory is what you are actually paying for, whether the invoice says so or not.

---
