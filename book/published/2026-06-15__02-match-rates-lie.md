<!-- Ready for Medium. Published 2026-06-15. Part of 'The Identity Layer' by Shubham Safaya. No em dashes. -->

# Match Rates Lie

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

*This essay is part of an ongoing series, [The Identity Layer](https://github.com/Shubham-Safaya/daily-engineering-log/tree/main/book), where I work out in public how customer identity, advertising, and privacy fit together. I am a Senior Product Manager at Walmart Global Tech. Follow on [LinkedIn](https://www.linkedin.com/in/shubham-safaya/).*
