# Who Is the Customer, Really?

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
