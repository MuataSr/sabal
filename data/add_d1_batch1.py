#!/usr/bin/env python3
"""Add 21 new D1 questions: Topics 1-3 (7 each: 1 easy, 3 medium, 3 hard)"""
import sqlite3, json
from datetime import datetime

db = sqlite3.connect('/home/muatasr/.nanobot/workspace/fcle-study-app/data/fcle.db')
cur = db.cursor()
ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

questions = [
    # === TOPIC: Citizen participation (7 new) ===
    {
        "fcle_domain": 1, "topic": "Citizen participation", "difficulty": "easy",
        "question": "Which form of political participation requires the least time commitment from a citizen?",
        "correct_answer": "Voting in a national election",
        "wrong_answers": json.dumps(["Organizing a local advocacy campaign", "Attending a city council meeting regularly", "Running for a partisan political office"]),
        "explanation": "Voting, while a fundamental act of citizenship, requires minimal ongoing time investment compared to organizing campaigns, attending regular meetings, or running for office. Research on political participation consistently shows that voting has the lowest barrier to entry among conventional political activities. Organizing campaigns and attending meetings require sustained engagement, while running for office demands months or years of full-time commitment.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Citizen participation", "difficulty": "medium",
        "question": "Political scientist Sidney Verba identified three resources that predict political participation: time, money, and civic skills. Which socioeconomic group typically possesses the greatest advantage across all three?",
        "correct_answer": "College-educated professionals",
        "wrong_answers": json.dumps(["Working-class union members", "Retirees with fixed incomes", "First-generation immigrants"]),
        "explanation": "Verba, Schlozman, and Brady's research in 'Voice and Equality' (1995) demonstrated that higher education and professional occupations provide citizens with all three participation resources: flexible schedules (time), higher incomes (money), and workplace-acquired skills like public speaking, organizing, and writing (civic skills). While union members may have civic skills and retirees have time, neither group consistently matches the across-the-board resource advantage held by college-educated professionals.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Citizen participation", "difficulty": "medium",
        "question": "The concept of 'political efficacy' has two dimensions: internal and external. Which scenario best illustrates a decline in external political efficacy?",
        "correct_answer": "A citizen who believes government is too corrupt to respond to any public pressure stops attending protests",
        "wrong_answers": json.dumps(["A citizen feels they lack the knowledge to understand ballot initiatives and skips voting", "A citizen moves to a new state and is unsure how to register to vote", "A citizen believes their single vote cannot change an election outcome"]),
        "explanation": "External political efficacy refers to the belief that the government will respond to citizens' demands. When a citizen perceives government as unresponsive or corrupt, external efficacy declines, reducing participation. Internal efficacy refers to self-confidence in understanding politics — a citizen who skips voting because they feel uninformed is experiencing low internal efficacy. Believing one's vote doesn't matter blends both dimensions but primarily reflects internal efficacy about personal impact.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Citizen participation", "difficulty": "medium",
        "question": "Which factor best explains why voter turnout in the United States is lower than in most other established democracies?",
        "correct_answer": "The United States places the burden of voter registration on individual citizens rather than the government",
        "wrong_answers": json.dumps(["The United States holds elections less frequently than other democracies", "American citizens face stricter eligibility requirements than voters abroad", "The U.S. uses a proportional representation system that discourages marginal voters"]),
        "explanation": "Comparative political scientists identify voter registration laws as a primary driver of the U.S. turnout gap. Most democracies use automatic or government-initiated registration, removing a significant participation barrier. The U.S. requires citizens to navigate registration procedures themselves, creating a 'cost' that depresses turnout, particularly among lower-income and younger citizens. The U.S. holds more frequent elections than most democracies (not fewer), eligibility requirements are generally less restrictive, and the U.S. does not use proportional representation.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Citizen participation", "difficulty": "hard",
        "question": "In their study of 'unconventional participation,' McAdam and Boudet found that communities facing environmental threats were more likely to engage in collective action when which condition was present?",
        "correct_answer": "Pre-existing social networks and community organizations provided mobilizing infrastructure",
        "wrong_answers": json.dumps(["The environmental threat was scientifically verified by federal agencies", "The affected community had higher-than-average median household income", "Local media outlets provided sustained investigative coverage of the threat"]),
        "explanation": "McAdam and Boudet's research on environmental justice movements emphasized that social networks and pre-existing organizational ties are the critical predictors of collective action, not the objective severity of the threat itself. Communities with churches, neighborhood associations, and civic groups already in place can more rapidly convert grievance into organized protest. This aligns with resource mobilization theory, which holds that social infrastructure matters more than the intensity of the grievance in predicting whether participation occurs.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Citizen participation", "difficulty": "hard",
        "question": "The National Voter Registration Act of 1993 ('Motor Voter Act') significantly increased registration rates but had a much smaller effect on actual turnout. Which explanation is most consistent with rational choice theory?",
        "correct_answer": "Registration is a necessary but not sufficient condition for turnout; lowering registration costs does not change the perceived cost-benefit calculation of voting itself",
        "wrong_answers": json.dumps(["The Act was undermined by state-level implementation that created new barriers replacing old ones", "Newly registered voters lacked the political knowledge to make informed choices at the ballot box", "The Act increased registration among demographics that were already likely to vote, creating a ceiling effect"]),
        "explanation": "Rational choice theory, as articulated by Anthony Downs, models voting as a cost-benefit calculation where citizens weigh the probability their vote matters against the costs of participation. The Motor Voter Act reduced one cost (registration) but did not change the fundamental calculus — voting still requires time, effort, and information. The 'paradox of voting' persists because the probability of being decisive remains vanishingly small regardless of registration ease. This explains why registration gains didn't translate proportionally into turnout gains.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Citizen participation", "difficulty": "hard",
        "question": "Piven and Cloward's 'Why Americans Don't Vote' argues that low turnout in the U.S. is best understood as:",
        "correct_answer": "A deliberate outcome of institutional design that historically excluded lower classes from electoral politics",
        "wrong_answers": json.dumps(["A reflection of widespread political satisfaction that reduces the urgency of participation", "A cultural artifact of individualism that makes collective political action seem foreign", "A rational response to the two-party system's failure to offer meaningful policy differences"]),
        "explanation": "Piven and Cloward's controversial thesis argues that American voter registration and election laws were not neutral administrative procedures but deliberate instruments of class control. They trace how voter registration requirements, residency laws, and literacy tests evolved to exclude working-class and immigrant voters. Unlike rational choice theorists who see low turnout as individual cost-benefit calculation, Piven and Cloward see it as structural exclusion embedded in institutional design — a fundamentally different causal explanation.",
        "stimulus": None
    },

    # === TOPIC: Federalism basics (7 new) ===
    {
        "fcle_domain": 1, "topic": "Federalism basics", "difficulty": "easy",
        "question": "Which level of government in the U.S. federal system is responsible for conducting foreign policy and negotiating treaties?",
        "correct_answer": "The national (federal) government",
        "wrong_answers": json.dumps(["State governments acting through interstate compacts", "Local governments through their international trade offices", "Both state and federal governments share this power equally"]),
        "explanation": "Under the U.S. Constitution, foreign policy and treaty-making are exclusively federal powers. The President negotiates treaties (with Senate ratification), and Congress regulates foreign commerce. States are constitutionally prohibited from conducting foreign policy — they cannot enter into treaties or alliances. While states may maintain trade offices abroad for economic development, this is not foreign policy in the constitutional sense.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Federalism basics", "difficulty": "medium",
        "question": "The Supreme Court's decision in United States v. Lopez (1995) is significant in federalism because it:",
        "correct_answer": "Established the first limits in decades on Congress's power under the Commerce Clause",
        "wrong_answers": json.dumps(["Confirmed that states could nullify federal laws they deemed unconstitutional", "Extended federal power to regulate all economic activities with even indirect effects on interstate commerce", "Required the federal government to fund all mandates imposed on state governments"]),
        "explanation": "Lopez was a landmark federalism case in which the Court struck down the Gun-Free School Zones Act, holding that possessing a gun near a school was not economic activity and therefore fell outside Congress's Commerce Clause authority. This was the first time since the New Deal era that the Court placed meaningful limits on the Commerce Clause, signaling a revival of dual federalism principles. It did not involve state nullification (which is unconstitutional post-McCulloch), nor did it extend federal power or address unfunded mandates.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Federalism basics", "difficulty": "medium",
        "question": "Cooperative federalism, which dominated from the 1930s through the 1960s, is best characterized by which feature?",
        "correct_answer": "Shared responsibilities between national and state governments with blurred jurisdictional boundaries",
        "wrong_answers": json.dumps(["Clear constitutional separation of powers between state and national governments", "State governments resisting federal expansion through coordinated legal challenges", "The complete transfer of most government functions from states to the federal level"]),
        "explanation": "Cooperative federalism emerged during the New Deal as the national and state governments increasingly worked together on policy problems. Unlike dual federalism, which maintained rigid boundaries between state and federal spheres, cooperative federalism involves overlapping responsibilities — both levels work on the same problems using grants, shared funding, and joint programs. It does not mean states surrendered all authority; rather, the lines between state and federal jurisdiction became blurred and intertwined.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Federalism basics", "difficulty": "medium",
        "question": "Block grants and categorical grants differ primarily in that block grants provide states with:",
        "correct_answer": "Greater flexibility in how funds are spent within a broad policy area",
        "wrong_answers": json.dumps(["More total funding than categorical grants for equivalent programs", "Guaranteed funding that cannot be reduced by future congressional action", "The ability to redirect funds to entirely different policy areas without federal oversight"]),
        "explanation": "Block grants provide federal funds to states for broad policy areas (like community development or public health) with fewer restrictions on spending. Categorical grants target specific purposes with detailed federal requirements. Block grants offer states flexibility in allocating resources, but they do not typically provide more funding than categorical grants, are not guaranteed against future cuts, and generally require funds to remain within the designated broad policy area.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Federalism basics", "difficulty": "hard",
        "question": "The concept of 'unfunded mandates' became a significant federalism issue in the 1990s, leading to the Unfunded Mandates Reform Act of 1995. Which constitutional provision do critics argue these mandates potentially violate?",
        "correct_answer": "The Tenth Amendment's reservation of powers to the states",
        "wrong_answers": json.dumps(["The Supremacy Clause's establishment of federal law as supreme", "The Commerce Clause's regulation of interstate economic activity", "The Necessary and Proper Clause's authorization of implied congressional powers"]),
        "explanation": "Critics of unfunded mandates argue that when Congress requires states to implement programs or meet standards without providing funding, it effectively commandeers state resources and violates the Tenth Amendment, which reserves powers not delegated to the federal government to the states. The Supreme Court reinforced this principle in Printz v. United States (1997) and New York v. United States (1992), holding that Congress cannot directly compel state officials to enforce federal regulatory programs. The Supremacy Clause actually supports federal mandates, and the Commerce Clause and Necessary and Proper Clause are sources of federal, not state, authority.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Federalism basics", "difficulty": "hard",
        "question": "In Printz v. United States (1997), the Supreme Court struck down provisions of the Brady Handgun Violence Prevention Act. The constitutional principle most central to this decision was:",
        "correct_answer": "The anti-commandeering doctrine prohibiting Congress from compelling state executive officials to enforce federal law",
        "wrong_answers": json.dumps(["The Second Amendment right to bear arms as an individual constitutional protection", "The Commerce Clause limitation on federal regulation of purely intrastate gun sales", "The Eleventh Amendment's protection of states from lawsuits by private citizens"]),
        "explanation": "Printz v. United States established that the federal government cannot compel state executive officers to implement federal regulatory programs. The Brady Act required local chief law enforcement officers to conduct background checks on handgun purchasers, which the Court ruled violated principles of state sovereignty. This 'anti-commandeering' doctrine was later reinforced in Murphy v. NCAA (2018). The case did not address the Second Amendment, Commerce Clause scope, or the Eleventh Amendment — it was fundamentally about federalism and the division of authority between national and state governments.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Federalism basics", "difficulty": "hard",
        "question": "Which of the following best explains why 'devolution' in the 1990s did not produce the dramatic shift in power to the states that its advocates predicted?",
        "correct_answer": "The federal government retained control through funding conditions attached to block grants, preserving de facto influence over state policy",
        "wrong_answers": json.dumps(["States lacked the administrative capacity and expertise to manage the programs transferred to them", "The Supreme Court struck down key devolution legislation as unconstitutional delegations of federal power", "Public opinion shifted against state-level control during economic recessions, forcing federal reassertion"]),
        "explanation": "Devolution — the transfer of program responsibility from federal to state governments — appeared to shift power through block grants and welfare reform. However, political scientists note that the federal government maintained substantial control by attaching conditions to funding. States that refused to comply with federal requirements risked losing grants, creating a compliance mechanism that preserved federal influence despite the formal transfer of authority. This illustrates the 'carrot and stick' dynamic: funding conditions can be as coercive as direct mandates, making true power transfer illusory.",
        "stimulus": None
    },

    # === TOPIC: Interest groups and lobbying (7 new) ===
    {
        "fcle_domain": 1, "topic": "Interest groups and lobbying", "difficulty": "easy",
        "question": "What is the primary difference between an interest group and a political party?",
        "correct_answer": "Interest groups focus on specific policy issues, while political parties seek to win elections and govern",
        "wrong_answers": json.dumps(["Interest groups are illegal under federal law, while political parties are constitutionally protected", "Political parties can only operate at the national level, while interest groups operate only locally", "Interest groups nominate candidates for office, while political parties only advocate for policies"]),
        "explanation": "The fundamental distinction is purpose and scope. Interest groups advocate for specific policies or interests (environmental protection, gun rights, healthcare) without nominating candidates. Political parties exist primarily to contest elections, nominate candidates, and organize government. Interest groups are legal and constitutionally protected under the First Amendment, and both types of organizations can operate at national, state, and local levels.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Interest groups and lobbying", "difficulty": "medium",
        "question": "Mancur Olson's 'logic of collective action' explains why large groups face greater difficulty organizing than small groups. What is the core of his argument?",
        "correct_answer": "In large groups, individuals can benefit from the group's success without contributing, creating a free-rider problem that undermines organizational efforts",
        "wrong_answers": json.dumps(["Large groups have more diverse interests that make consensus on policy goals impossible to achieve", "The government actively suppresses large organizations while allowing smaller groups to form freely", "Large groups inherently lack the leadership and organizational skills needed for effective political action"]),
        "explanation": "Olson's central insight is that collective action problems intensify with group size. In a small group, each member's contribution is visible and significant, making participation rational. In a large group, the benefit of any individual's contribution is negligible to the overall outcome, so rational actors free-ride — enjoying benefits others produce without contributing themselves. This explains why concentrated interests (small groups with high stakes) often prevail over diffuse interests (large groups with dispersed stakes) in the political process.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Interest groups and lobbying", "difficulty": "medium",
        "question": "An 'iron triangle' in American politics refers to the close relationship among which three actors?",
        "correct_answer": "A congressional committee, a bureaucratic agency, and an interest group",
        "wrong_answers": json.dumps(["The President, the Speaker of the House, and the Chief Justice of the Supreme Court", "A political party, a media outlet, and a polling organization", "A state governor, a federal district court, and a regional planning commission"]),
        "explanation": "The iron triangle model describes a stable, mutually beneficial relationship between a congressional committee (which provides funding and oversight), a bureaucratic agency (which implements policy and provides expertise), and an interest group (which provides political support and information). Each actor benefits: the committee gets expertise and constituency service, the agency gets budgetary support and political protection, and the interest group gets favorable policy outcomes. Critics argue this model oversimplifies modern policy-making, where issue networks and multiple competing interests are more common.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Interest groups and lobbying", "difficulty": "medium",
        "question": "Which of the following is the most common method interest groups use to influence the judicial branch?",
        "correct_answer": "Filing amicus curiae ('friend of the court') briefs in cases relevant to their policy interests",
        "wrong_answers": json.dumps(["Directly lobbying individual Supreme Court justices in private meetings", "Sponsoring judicial candidates in partisan primary elections", "Controlling the docket schedule of federal appellate courts through procedural motions"]),
        "explanation": "Interest groups seeking to influence judicial outcomes most commonly file amicus curiae briefs, which present arguments and information relevant to a case without being a direct party to it. These briefs allow groups to shape legal reasoning and expose the Court to policy perspectives. Direct lobbying of sitting judges is prohibited by judicial ethics rules, judicial elections are limited to state courts, and interest groups have no control over federal court dockets. Amicus briefs have become increasingly influential as the Court has granted more organizations standing to file them.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Interest groups and lobbying", "difficulty": "hard",
        "question": "The 'revolving door' phenomenon — where officials move between government positions and private sector lobbying — is best understood as a problem of which type?",
        "correct_answer": "Regulatory capture, where agencies develop priorities that align with the industries they regulate",
        "wrong_answers": json.dumps(["Logrolling, where legislators exchange votes on unrelated bills to secure mutual support", "Gerrymandering, where electoral districts are drawn to favor specific political parties", "Judicial activism, where courts overturn legislative decisions based on policy preferences rather than law"]),
        "explanation": "The revolving door contributes to regulatory capture — a concept described by economists including George Stigler. When regulators and industry representatives move fluidly between sectors, agencies may develop sympathetic relationships with the industries they oversee, leading to rulemaking that favors regulated entities over the public interest. This is distinct from logrolling (legislative vote trading), gerrymandering (district manipulation), and judicial activism (court overreach) — the revolving door specifically describes personnel flows that bias regulatory outcomes.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Interest groups and lobbying", "difficulty": "hard",
        "question": "Grutter v. Bollinger (2003) allowed universities to consider race in admissions. Why were interest group filings in this case considered strategically significant beyond their legal arguments?",
        "correct_answer": "The breadth of the amicus coalition signaled to the Court the institutional weight behind affirmative action, affecting the perceived legitimacy of the outcome",
        "wrong_answers": json.dumps(["The interest groups provided the primary constitutional arguments that the parties themselves failed to raise", "The case was entirely funded by interest groups who effectively acted as the real parties in interest", "Interest group lobbying of individual justices prior to oral argument determined the Court's deliberation strategy"]),
        "explanation": "In Grutter, dozens of amicus briefs were filed by universities, corporations, military leaders, and civil rights organizations. Political scientists studying the Court note that the breadth and diversity of this coalition served a signaling function — it demonstrated to the Court that affirmative action had support across major institutions, not just among advocacy groups. This coalition-building strategy aimed to show that overturning affirmative action would disrupt established institutional practices, making the Court more cautious. The interest groups did not provide primary legal arguments, fund the case, or lobby justices directly.",
        "stimulus": None
    },
    {
        "fcle_domain": 1, "topic": "Interest groups and lobbying", "difficulty": "hard",
        "question": "Political scientists debate whether 'campaign contributions buy access or votes.' The preponderance of empirical evidence on contributions to members of Congress suggests they primarily affect:",
        "correct_answer": "Access to legislators and the opportunity to present a group's perspective, rather than direct vote switching",
        "wrong_answers": json.dumps(["Legislators' votes on the specific bills that the contributing interest group cares about", "Committee assignments and leadership positions within the chamber", "The likelihood that a legislator will introduce original legislation drafted by the interest group"]),
        "explanation": "Extensive political science research (including studies by Richard Hall and Frank Wayman) finds that campaign contributions are more strongly correlated with access than with vote changes. Contributors gain meetings, have their calls returned, and get opportunities to present their views during legislative deliberation. While this access advantage is not trivial, studies consistently show that legislators' voting behavior is more strongly predicted by party, ideology, and constituency interests than by campaign money. This finding challenges the popular assumption that contributions directly 'buy votes' — the mechanism is more subtle and indirect.",
        "stimulus": None
    },
]

for q in questions:
    cur.execute('''
        INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation, stimulus, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (q['fcle_domain'], q['topic'], q['difficulty'], q['question'], q['correct_answer'],
          q['wrong_answers'], q['explanation'], q['stimulus'], ts))

db.commit()
print(f"Inserted {len(questions)} D1 questions (batch 1: Citizen participation, Federalism basics, Interest groups)")
db.close()
