#!/usr/bin/env python3
"""Add 28 new D1 questions: Topics 7-10 (7 each: 1 easy, 3 medium, 3 hard)"""
import sqlite3, json
from datetime import datetime, timezone

db = sqlite3.connect('/home/muatasr/.nanobot/workspace/fcle-study-app/data/fcle.db')
cur = db.cursor()
ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
WA = json.dumps

Q = [
    # TOPIC: Political culture and ideology
    (1, "Political culture and ideology", "easy",
     "Political culture refers to:",
     "The shared beliefs, values, and attitudes that citizens hold about government and politics",
     WA(["The formal legal structure of government institutions and the constitution", "The specific policy positions that political parties adopt during election campaigns", "The process by which citizens develop their individual political preferences over time"]),

     "Political culture is the set of shared attitudes, beliefs, and values that shape how a society relates to its government. It includes expectations about how government should function, citizens role in politics, and the proper relationship between the state and individuals. American political culture, for example, emphasizes individual liberty, equality of opportunity, and distrust of concentrated power. It differs from political structure (the formal design of institutions) and political ideology (coherent belief systems about the proper scope of government)."),
    (1, "Political culture and ideology", "medium",
     "Daniel Elazar identified three types of American political culture: individualistic, moralistic, and traditionalistic. The moralistic political culture, most prevalent in New England and the Upper Midwest, is characterized by:",
     "The belief that government should actively promote the public good and that political participation is a civic duty",
     WA(["The view that government intervention in the economy should be minimized and markets left alone", "The expectation that politics is reserved for an established elite and that ordinary citizens should defer to their leadership", "The belief that government exists primarily to serve the private interests of those who hold office"]),

     "Elazar moralistic political culture views government as a positive force for advancing the common good. Citizens in moralistic culture regions expect government to serve the public interest, value broad political participation, and are more tolerant of higher taxes for public services. Individualistic culture (Mid-Atlantic, Midwest) sees politics as a marketplace for pursuing private interests with minimal government interference. Traditionalistic culture (South) maintains hierarchical social structures and expects politics to be managed by established elites. These cultural patterns persist across policy preferences and civic engagement levels."),
    (1, "Political culture and ideology", "medium",
     "Classical liberalism, which forms a core component of American political culture, differs from modern American liberalism primarily in its emphasis on:",
     "Limited government and individual economic freedom as the primary means to protect liberty",
     WA(["Government regulation of the economy to ensure fair outcomes for all citizens", "Collective action through labor unions and community organizations to achieve social goals", "Strong executive authority to maintain social order and national security"]),

     "Classical liberalism, rooted in Locke and Smith, prioritizes individual liberty, limited government, free markets, and property rights as the foundations of a free society. Modern American liberalism retains classical liberal commitments to civil liberties but supports a more active government role in regulating the economy, providing social safety nets, and promoting equality of opportunity. The key difference is the view of government: classical liberalism sees it as a potential threat to liberty, while modern liberalism sees it as a potential instrument for expanding liberty and opportunity."),
    (1, "Political culture and ideology", "medium",
     "The concept of 'American exceptionalism' in political culture refers to:",
     "The belief that the United States has a unique role and destiny among nations, rooted in its founding ideals of liberty and democracy",
     WA(["The empirical observation that American political institutions function more effectively than those of other democracies", "The constitutional principle that the Supreme Court can declare laws unconstitutional", "The economic advantage the United States enjoys due to its geographic isolation and abundant natural resources"]),

     "American exceptionalism is the belief that the United States is qualitatively different from other nations because of its founding principles, revolutionary origins, and commitment to individual liberty. This concept, articulated by Alexis de Tocqueville and later political scientists, holds that America has a unique mission to model democratic governance. It is a cultural belief, not an empirical claim about institutional effectiveness or economic advantage. Critics note that exceptionalist thinking can lead to foreign policy overreach and blind spots about America own historical failings."),
    (1, "Political culture and ideology", "hard",
     "Political scientists have documented increasing ideological polarization in Congress since the 1970s. Which structural factor has most contributed to this trend?",
     "The realignment of the South from Democratic to Republican, which removed a cross-cutting conservative faction from the Democratic Party",
     WA(["The introduction of television advertising that allowed candidates to bypass party organizations", "The growing influence of corporate lobbying that pushed both parties toward business-friendly policies", "The decline of labor union membership that removed a unifying economic issue from political debate"]),

     "The most significant structural driver of Congressional polarization was the Southern realignment. Before the 1970s, the Democratic Party contained both Northern liberals and Southern conservatives, creating ideological overlap with Republicans and producing cross-party coalitions. As Southern whites shifted to the Republican Party (accelerated by Civil Rights legislation), both parties became more ideologically homogeneous. Nolan McCarty, Keith Poole, and Howard Rosenthal research shows this realignment accounts for the majority of the increase in ideological distance between the parties, more than media changes, lobbying, or union decline."),
    (1, "Political culture and ideology", "hard",
     "Social identity theory provides an alternative explanation for partisan behavior, suggesting that:",
     "Party identification functions more as a group identity and source of self-esteem than as a rational evaluation of policy positions",
     WA(["Voters systematically update their ideological positions based on new information about party platforms", "Partisan loyalty is primarily driven by economic self-interest and expected material benefits from policy outcomes", "Political socialization in early adulthood permanently fixes an individual partisan affiliation regardless of later experiences"]),

     "Social identity theory, applied to politics by scholars like Donald Green, Bradley Palmquist, and Eric Schickler, argues that party identification operates as a social identity similar to ethnic or religious identity. Partisans derive self-esteem from their group membership and are motivated to defend their in-group against out-groups. This explains why partisans often cannot articulate their party policy positions, why they resist information threatening their partisan identity, and why partisan identity often persists even when policy positions change. It challenges the rational choice view of partisanship as primarily policy-driven."),
    (1, "Political culture and ideology", "hard",
     "The concept of 'intersectionality,' originally developed in legal scholarship, has implications for understanding American political culture because it:",
     "Reveals how overlapping social identities (race, class, gender) create distinct political experiences that cannot be understood by examining any single identity category alone",
     WA(["Demonstrates that economic class has become the dominant predictor of voting behavior in the 21st century", "Proves that identity-based political mobilization inevitably fragments the progressive coalition", "Shows that racial identity has replaced class identity as the primary axis of political conflict in America"]),

     "Intersectionality, developed by Kimberle Crenshaw, holds that systems of oppression and identity cannot be understood in isolation. In political culture, this means that a working-class Black woman political experience is shaped by the interaction of race, class, and gender in ways that studying any one dimension alone misses. This framework challenges traditional political science categories that treat identity variables as independent and additive. It does not claim class is the dominant predictor, that identity politics inevitably fragments coalitions, or that race has simply replaced class as the primary axis of conflict."),

    # TOPIC: Political parties and elections
    (1, "Political parties and elections", "easy",
     "What is the primary function of a political party in the American political system?",
     "To recruit candidates, organize elections, and coordinate policy agendas for governing",
     WA(["To enforce the laws passed by Congress and signed by the President", "To interpret the Constitution and determine the constitutionality of federal laws", "To represent foreign governments in diplomatic negotiations with the United States"]),

     "Political parties serve as linkage institutions connecting citizens to government. Their core functions include recruiting and nominating candidates, organizing electoral campaigns, coordinating legislative agendas, and providing a mechanism for collective governance. Unlike interest groups, parties seek to control government by winning elections and holding office. Law enforcement is the executive branch role, constitutional interpretation belongs to the judiciary, and diplomatic representation is conducted by the State Department, not political parties."),
    (1, "Political parties and elections", "medium",
     "The concept of 'critical elections' in realignment theory refers to elections that:",
     "Produce a lasting shift in the coalition of groups supporting each political party, fundamentally altering the party system",
     WA(["Are decided by the smallest margin of victory in American electoral history", "Feature the highest voter turnout rates among eligible citizens", "Result in the election of a third-party candidate to the presidency"]),

     "Critical election theory, developed by V.O. Key, identifies certain elections as turning points that fundamentally restructure the party system. These elections create new, durable coalitions that persist for decades. Examples include 1860 (Republicans rise, Civil War alignment), 1896 (Republican dominance of industrial era), and 1932 (New Deal realignment). Critical elections are defined by sharp and lasting changes in voter loyalty patterns, not by close margins, high turnout, or third-party victories, though these may accompany realignments."),
    (1, "Political parties and elections", "medium",
     "The use of primary elections to select party nominees, rather than party leaders choosing candidates in caucuses or conventions, has had which effect on American politics?",
     "It has weakened party organizations by shifting candidate selection power from party elites to the general electorate",
     WA(["It has increased the ideological cohesion of both major parties by ensuring nominees reflect mainstream voter preferences", "It has decreased the cost of running for office by eliminating the need for campaign fundraising", "It has reduced the influence of incumbency advantage in congressional elections"]),

     "The shift from party-controlled nomination processes to primary elections (accelerated by progressive era reforms and the McGovern-Fraser Commission after 1968) transferred candidate selection from party elites to voters. This weakened party organizations because they lost control over who carries their banner. Critics argue primaries incentivize candidates to appeal to the more ideologically extreme primary electorate rather than the general electorate, potentially contributing to polarization. The reform did not reduce campaign costs or diminish incumbency advantage; in fact, incumbents typically dominate primaries."),
    (1, "Political parties and elections", "medium",
     "The Electoral College system can produce a president who did not win the national popular vote because:",
     "Electors are allocated on a winner-take-all basis in 48 states, so a candidate can win key states by narrow margins while losing the national popular vote",
     WA(["The Constitution requires electors to vote for the candidate who won their state popular vote regardless of the national outcome", "The Electoral College gives each state an equal number of votes regardless of population", "Third-party candidates can win electoral votes by achieving a plurality in enough states"]),

     "The Electoral College can produce a split result because 48 states award all their electors to the statewide popular vote winner (winner-take-all). A candidate can win decisive victories in large states by narrow margins while losing badly in others, accumulating electoral votes without a popular majority. This occurred in 1876, 1888, 2000, and 2016. The system does not give states equal votes (small states get proportionally more per capita but large states dominate with more total electors), does not constitutionally require electors to follow the popular vote (though most states bind them), and third parties rarely win electoral votes."),
    (1, "Political parties and elections", "hard",
     "Morris Fiorina argument in 'Divided Government' suggests that split-ticket voting (voting for different parties for president and Congress) reflects:",
     "Rational voter preference for institutional balance rather than confusion or declining partisanship",
     WA(["Voter ignorance about the policy positions of candidates from different parties", "The declining relevance of political parties as organizations that structure voter choices", "Deliberate manipulation of ballot design by party leaders to confuse elderly voters"]),

     "Fiorina argued that divided government (one party controlling the presidency, the other Congress) is not a sign of voter confusion but a rational strategy. Voters who prefer moderation can achieve policy balance by splitting their votes, preventing either party from implementing its full agenda. This explains why divided government has been common in the postwar era. Fiorina thesis challenged the realignment model and the assumption that straight-ticket voting indicates healthy partisanship. He suggested that divided government is a mechanism through which moderate voters express preferences in a two-party system."),
    (1, "Political parties and elections", "hard",
     "In redistricting, 'packing and cracking' are gerrymandering strategies. Which combination best describes how they work together to disadvantage a target group?",
     "Packing concentrates the target group voters into few districts to waste their surplus votes, while cracking disperses remaining target voters across multiple districts where they cannot achieve a majority",
     WA(["Packing distributes target group voters evenly across all districts to dilute their collective influence, while cracking creates majority-minority districts that isolate them politically", "Both packing and cracking involve drawing district boundaries to follow natural geographic features like rivers and county lines", "Packing creates competitive districts that encourage turnout, while cracking creates safe districts that discourage opposition participation"]),

     "The two primary gerrymandering techniques work in tandem. Packing concentrates opposition voters into a small number of districts where they win overwhelmingly, wasting their surplus votes that could have helped them win additional districts. Cracking takes the remaining opposition voters and scatters them across many districts at levels below 50 percent, ensuring they cannot elect their preferred candidates. Together, these strategies can translate a substantial minority (or even majority) of statewide support into very few seats. The Supreme Court addressed racial gerrymandering but has struggled to establish justiciable standards for partisan gerrymandering."),
    (1, "Political parties and elections", "hard",
     "The concept of 'dealignment' in party politics refers to:",
     "A decline in long-term party loyalty among voters, leading to increased ticket-splitting, independent identification, and volatility in election outcomes",
     WA(["The process by which a political party abandons its traditional platform positions to attract new voter demographics", "A strategic decision by party leaders to reduce the ideological distance between the two major parties", "The institutional decay of party organizations due to campaign finance reforms that shifted power to candidates"]),

     "Dealignment, identified by political scientists in the 1970s and 1980s, describes the erosion of strong party identification among American voters. As fewer voters identify strongly with either party, more identify as independents, split tickets between parties, and make election choices based on candidate characteristics or specific issues rather than party loyalty. This differs from realignment (a shift from one stable alignment to another) because dealignment involves moving away from parties altogether rather than switching allegiance. Dealignment increases electoral volatility and complicates party strategy."),

    # TOPIC: Political socialization
    (1, "Political socialization", "easy",
     "Which of the following is typically the earliest and most influential agent of political socialization in a person life?",
     "The family",
     WA(["Public education and schools", "Social media and the internet", "Religious institutions and churches"]),

     "Political socialization is the lifelong process through which individuals develop their political attitudes and values. Research consistently shows that the family is the primary agent of early political socialization. Children often adopt their parents party identification, attitudes toward government, and issue positions through observation, conversation, and shared experiences. While schools, media, and religious institutions become more influential later, the family establishes the initial political framework. Studies show that approximately two-thirds of young adults share their parents party identification."),
    (1, "Political socialization", "medium",
     "The 'generational effect' in political socialization refers to:",
     "The lasting impact of major political events that occur during a cohort formative years on their lifelong political attitudes",
     WA(["The tendency of each successive generation to adopt more progressive political views than their parents", "The increasing influence of digital media on younger generations compared to older ones", "The cyclical pattern where political attitudes alternate between liberal and conservative across generations"]),

     "Generational effects occur when significant historical events shape the political outlook of an entire age cohort. The Great Depression generation developed lasting Democratic loyalty; the Vietnam and Watergate era shaped the political skepticism of Baby Boomers; 9/11 influenced Millennial attitudes toward national security. These effects persist because formative experiences during late adolescence and early adulthood establish durable political frameworks. Generational effects differ from lifecycle effects (attitudes changing as individuals age) and period effects (temporary shifts affecting all generations simultaneously)."),
    (1, "Political socialization", "medium",
     "Research on political socialization through education suggests that the primary political effect of formal schooling is:",
     "Increased political knowledge and civic skills rather than a predictable shift in specific political attitudes or party identification",
     WA(["A systematic shift toward liberal or progressive political views regardless of the curriculum taught", "The reinforcement of conservative values through the hidden curriculum of discipline and authority", "The elimination of parental political influence through exposure to diverse viewpoints in the classroom"]),

     "Extensive research on education and political socialization finds that formal schooling primarily increases political knowledge, tolerance of opposing viewpoints, and civic participation skills. However, it does not reliably produce specific ideological shifts in either direction. The claim that education systematically produces liberals (a common conservative critique) or that schools exist to indoctrinate is not supported by empirical evidence. Education appears to make citizens more informed and engaged, but their ideological direction depends on many factors beyond schooling, including family, peers, and personal experience."),
    (1, "Political socialization", "medium",
     "The concept of a 'gender gap' in American voting behavior refers to the pattern where:",
     "Women are more likely than men to support Democratic candidates, while men are more likely to support Republican candidates",
     WA(["Female candidates consistently receive fewer votes than male candidates with equivalent qualifications", "Women vote at lower rates than men across all demographic groups and election types", "The gender gap has remained constant in magnitude since women gained the right to vote in 1920"]),

     "The gender gap in American politics, first prominently identified in the 1980 election, describes the tendency of women to favor Democratic candidates and men to favor Republicans. This gap has persisted and even widened in recent decades, driven by differences in attitudes toward social welfare, gun control, healthcare, and government role. It is important to distinguish this from the gender gap in candidate preference (women supporting female candidates), which is much smaller. Women vote at slightly higher rates than men, and the partisan gender gap was not constant but emerged and grew during the 1980s."),
    (1, "Political socialization", "hard",
     "Converse concept of 'non-attitudes' challenges the assumption that survey responses reflect stable, genuine policy preferences. His research suggested that:",
     "Many citizens lack meaningful, consistent ideological structures and instead construct responses on the spot based on question wording and context",
     WA(["All political attitudes are genetically determined and remain fixed throughout an individual lifetime", "Citizens hold deeply consistent policy positions that party platforms fail to adequately represent", "Survey non-response is the most reliable indicator of genuine political attitudes because only informed citizens choose to answer"]),

     "Philip Converse seminal 1964 study found that most citizens do not hold ideologically constrained belief systems. Instead, many survey responses are non-attitudes, constructed ad hoc in response to specific questions rather than reflecting pre-existing, stable preferences. This finding challenged rational models of democracy that assumed an informed, ideologically coherent electorate. Converse distinguished between the ideologically sophisticated minority who organize their political views into coherent structures and the majority who respond to politics through group identifications, candidate personalities, and immediate circumstances."),
    (1, "Political socialization", "hard",
     "The 'sibling effect' in political socialization research reveals that siblings who grow up in the same household often develop different political orientations. Which factor best explains this finding?",
     "Siblings experience shared family environments differently based on birth order, age gaps, and differing life experiences that occur outside the family",
     WA(["Genetic differences between siblings override shared environmental influences in determining political attitudes", "The political socialization process only operates effectively during the first five years of a child life", "Schools and media provide contradictory information that completely negates family political influence"]),

     "Research on sibling political differences demonstrates that shared family environment is not determinative of political attitudes. Siblings often diverge politically because birth order creates different parental relationship dynamics, age gaps mean siblings experience different historical events during their formative years, and peer groups, teachers, and life events differ between siblings. This finding complicates both pure family-determinism models and pure genetics models. It suggests that political socialization is an interactive process where the same household produces different outcomes based on individual positioning within that household."),
    (1, "Political socialization", "hard",
     "Zaller Receive-Accept-Sample (RAS) model of public opinion formation argues that an individual response to a political message depends on:",
     "Whether they receive the message, whether they accept it as true given their prior beliefs, and what sample of considerations comes to mind when expressing an opinion",
     WA(["Their level of formal education, which determines their ability to comprehend complex policy arguments", "The credibility of the media source, which is the single strongest predictor of opinion formation", "Their economic self-interest, which systematically overrides ideological predispositions in policy evaluation"]),

     "Zaller RAS model (1992) provides a sophisticated account of opinion formation. Reception depends on political awareness and media exposure. Acceptance depends on whether the message is consistent with prior political predispositions. Sampling means that the specific considerations that come to mind at the moment of response can vary, producing apparent instability in opinions. The model explains why more politically aware individuals show greater attitude constraint (their prior beliefs more consistently filter information) and why survey responses can fluctuate without any genuine attitude change. It challenges simple models based on education, source credibility, or economic self-interest alone."),

    # TOPIC: Popular sovereignty
    (1, "Popular sovereignty", "easy",
     "The principle of popular sovereignty in the U.S. political system means that:",
     "The authority of government is created and sustained by the consent of its people, through their elected representatives",
     WA(["Citizens vote directly on all major laws and policies without representation", "The Supreme Court has the final authority to determine what the people want", "State governments have more power than the federal government because they are closer to the people"]),

     "Popular sovereignty holds that all legitimate government authority derives from the people. In the U.S. system, this principle operates primarily through representative democracy, citizens elect officials who make decisions on their behalf. The Constitution preamble, We the People, embodies this concept. It does not mean direct democracy (citizens voting on all laws), judicial supremacy (the Court interpreting popular will), or state supremacy over federal power. Popular sovereignty is channeled through elections, representation, and the constitutional amendment process."),
    (1, "Popular sovereignty", "medium",
     "The initiative and referendum process, adopted by many states during the Progressive Era, represents an expansion of popular sovereignty by:",
     "Allowing citizens to directly propose and vote on laws and constitutional amendments, bypassing the state legislature",
     WA(["Replacing representative democracy with direct democracy at the state level entirely", "Giving state governors the power to override legislative decisions through executive orders", "Establishing independent commissions to redraw electoral districts instead of state legislatures"]),

     "The initiative allows citizens to collect signatures to place proposed laws or constitutional amendments directly on the ballot. The referendum allows citizens to vote to approve or reject laws passed by the legislature. Both mechanisms, adopted during the Progressive Era as reforms against corrupt state legislatures, expand direct citizen participation beyond representative institutions. They do not replace representative government entirely; states with initiative and referendum still have legislatures, governors, and courts. Independent redistricting commissions are a separate reform addressing gerrymandering."),
    (1, "Popular sovereignty", "medium",
     "James Madison expressed concern about pure popular sovereignty in Federalist No. 10 by warning against the:",
     "Tyranny of the majority, where a majority faction could suppress the rights of minorities",
     WA(["Concentration of power in the executive branch that could undermine democratic accountability", "Corrupting influence of political parties on the electoral process and legislative deliberation", "Danger of foreign interference in domestic elections through campaign contributions and propaganda"]),

     "Madison Federalist No. 10 identified faction (a group united by a common interest adverse to the rights of others) as the greatest threat to popular government. He argued that pure democracy, where the majority rules directly, offers no protection against majority tyranny because the majority can simply outvote minorities. Madison solution was a large republic with representative government, where the diversity of interests and geographic spread would make it difficult for any single faction to dominate. His argument for a republic over a pure democracy remains foundational to understanding the American constitutional system."),
    (1, "Popular sovereignty", "medium",
     "The concept of 'concurrent majority,' proposed by John C. Calhoun as an alternative to simple majority rule, argued that:",
     "Significant minority interests (particularly Southern states) should have an effective veto over national policy through concurrent regional majorities",
     WA(["All legislation should require a two-thirds supermajority to protect minority interests", "The Electoral College should be abolished in favor of direct popular election of the president", "States should be able to nullify federal laws they consider unconstitutional within their borders"]),

     "Calhoun concurrent majority theory held that no law should be enacted without the consent of all major interests in society. In practice, this meant giving regional minorities (specifically the slaveholding South) a veto over national policy. Calhoun developed this theory to protect Southern interests against a growing Northern majority. It differs from simple supermajority requirements because it demands concurrent approval from each interest group, not just a higher threshold of overall votes. While related to nullification (which Calhoun also advocated), concurrent majority was a broader theoretical framework for structuring government to protect minority rights against majority rule."),
    (1, "Popular sovereignty", "hard",
     "Robert Dahl concept of polyarchy describes a system that approximates popular sovereignty through which institutional features?",
     "Elected officials, free and fair elections, inclusive suffrage, the right to run for office, freedom of expression, alternative information sources, and associational autonomy",
     WA(["Direct democracy mechanisms including referendums, recalls, and citizen-initiated legislation at all levels of government", "A bicameral legislature with equal representation for all states regardless of population", "A judicial system with the power of judicial review over all legislative and executive actions"]),

     "Dahl polyarchy (1971) identifies seven institutions that, together, approximate democratic governance: elected officials, free and fair elections, inclusive citizenship, the right to run for office, freedom of expression, access to alternative sources of information, and associational autonomy (freedom to form organizations). Dahl deliberately used the term polyarchy rather than democracy to distinguish real-world approximations from the ideal of full popular sovereignty. These criteria allow comparison across regimes and have become standard metrics in comparative politics. They do not require direct democracy, equal state representation, or judicial supremacy."),
    (1, "Popular sovereignty", "hard",
     "The tension between popular sovereignty and constitutional limits is illustrated by the fact that:",
     "The Constitution can be amended only through a supermajority process that makes it difficult for temporary majorities to alter fundamental rights",
     WA(["The Supreme Court has the power to add new amendments to the Constitution through judicial decisions", "State legislatures can override federal constitutional provisions through interstate compacts", "The President can issue executive orders that modify constitutional requirements during national emergencies"]),

     "The U.S. Constitution embodies the tension between popular sovereignty (government derives its authority from the people) and constitutionalism (government power is limited by fundamental law). Amendment requires either a two-thirds vote in both houses of Congress plus ratification by three-fourths of states, or a constitutional convention called by two-thirds of states. This supermajority requirement ensures that temporary majorities cannot easily alter the fundamental rules of government or eliminate rights protections. This design deliberately makes popular sovereignty a constrained force, channeled through institutional mechanisms that prevent rapid, sweeping changes to the constitutional framework."),
    (1, "Popular sovereignty", "hard",
     "Jeremy Bentham dismissed the concept of natural rights as 'nonsense upon stilts' and argued instead that popular sovereignty should be grounded in:",
     "Utilitarian principles where government legitimacy derives from its ability to maximize happiness for the greatest number of people",
     WA(["Divine right, where government authority flows from religious rather than secular sources", "Historical tradition, where sovereignty is justified by the longevity and continuity of existing institutions", "Technocratic expertise, where governance should be delegated to specialists rather than elected representatives"]),

     "Bentham, founder of modern utilitarianism, rejected natural rights as metaphysical fictions with no empirical basis. Instead, he argued that legitimate government should be judged by its consequences, specifically its ability to maximize overall happiness and minimize suffering (the principle of utility). This utilitarian foundation for popular sovereignty differs from natural rights theory because it evaluates government by outcomes rather than by adherence to pre-existing rights. It also differs from divine right, historical tradition, and technocratic governance as justifications for political authority."),
]

for q in Q:
    cur.execute('INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation, stimulus, created_at) VALUES (?,?,?,?,?,?,?,NULL,?)', (q[0], q[1], q[2], q[3], q[4], q[5], q[6], ts))

db.commit()
print(f"Inserted {len(Q)} D1 questions (batch 3: Political culture, Parties, Socialization, Popular sovereignty)")
db.close()
