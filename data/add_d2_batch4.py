#!/usr/bin/env python3
"""Add D2 questions batch 4: 30 more (heavy on hard) to reach 150."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Hard: deeper constitutional principles (10)
    (2, "Constitutional principles", "hard",
     "What is the doctrine of 'originalism' in constitutional interpretation, and who is its most prominent modern advocate?",
     "Originalism holds that the Constitution should be interpreted based on its original public meaning at the time of ratification; Justice Antonin Scalia was its most prominent advocate.",
     json.dumps(["Originalism holds that the Constitution should be reinterpreted every generation to reflect modern values.",
                  "Originalism holds that only the President can interpret the Constitution.",
                  "Originalism is the doctrine that state constitutions override the federal Constitution."]),
     "Originalism is a theory of constitutional interpretation that argues the meaning of the Constitution should be determined by the original public understanding at the time it was adopted. Justice Antonin Scalia was the modern judicial movement's most prominent advocate, arguing that the Constitution's meaning is fixed and should not evolve with judges' personal preferences. Critics argue originalism can produce unjust outcomes because it ties interpretation to 18th-century understandings of concepts like 'cruel and unusual punishment' or 'equal protection.' Justice Scalia distinguished original meaning (what the text meant to the public) from original intent (what the Framers subjectively intended)."),

    (2, "Constitutional principles", "hard",
     "What is 'judicial activism' versus 'judicial restraint,' and why is this distinction politically contested?",
     "Judicial activism refers to courts striking down laws and creating new rights; judicial restraint refers to courts deferring to the elected branches. The distinction is contested because 'activism' often means 'rulings I disagree with.'",
     json.dumps(["Judicial activism means judges only handle criminal cases; judicial restraint means judges only handle civil cases.",
                  "Both terms refer to the same concept and are used interchangeably.",
                  "Judicial activism is a liberal concept; judicial restraint is a conservative concept, and neither side ever crosses over."]),
     "Judicial activism describes a judicial philosophy where courts are willing to strike down legislative and executive actions and to recognize rights not explicitly stated in the Constitution. Judicial restraint favors deferring to the political branches and limiting judicial intervention. The distinction is politically contested because conservatives call liberal rulings 'activist' (e.g., Roe v Wade) while liberals call conservative rulings 'activist' (e.g., Bush v Gore, Citizens United). In practice, both liberal and conservative justices engage in both activism and restraint depending on the issue."),

    (2, "Constitutional principles", "hard",
     "What is the 'political question doctrine,' and how does it limit judicial power?",
     "The political question doctrine holds that certain issues are constitutionally committed to the political branches and are not appropriate for judicial resolution.",
     json.dumps(["The political question doctrine requires all Supreme Court justices to be elected by popular vote.",
                  "The political question doctrine allows courts to decide any political dispute regardless of constitutional text.",
                  "The political question doctrine was created by the Second Amendment and applies only to gun rights cases."]),
     "The political question doctrine, established in Baker v Carr (1962), holds that certain constitutional issues should be resolved by the political branches (Congress and the President) rather than by courts. The Court identified several factors that may make an issue a political question: a textually demonstrated constitutional commitment to another branch, a lack of judicially manageable standards, or the impossibility of deciding without a policy determination. The doctrine is applied rarely but has been invoked in cases involving foreign policy, impeachment, and the apportionment of congressional districts."),

    (2, "Constitutional principles", "hard",
     "How does the 'doctrine of unconstitutional conditions' limit government power?",
     "The government cannot condition a benefit on the recipient giving up a constitutional right that the government could not directly take away.",
     json.dumps(["The doctrine requires all government conditions to be approved by a constitutional convention.",
                  "The doctrine prohibits any conditions on government benefits whatsoever.",
                  "The doctrine allows the government to impose any conditions it chooses on federal benefits."]),
     "The unconstitutional conditions doctrine holds that the government cannot grant a benefit on the condition that the recipient surrender a constitutional right that the government could not directly compel them to give up. For example, the government cannot provide unemployment benefits on the condition that recipients waive their right to free speech. The doctrine balances the government's interest in attaching reasonable conditions to benefits against individuals' constitutional rights. However, the Supreme Court has applied the doctrine inconsistently, making its exact scope difficult to define."),

    (2, "Constitutional principles", "hard",
     "What is the 'unitary executive theory' and how does it affect presidential power?",
     "The unitary executive theory holds that the President has complete control over the executive branch, including the power to remove any executive official and to direct how laws are interpreted and enforced.",
     json.dumps(["The unitary executive theory holds that all three branches of government are merged into one.",
                  "The unitary executive theory was rejected by the Supreme Court and has no legal standing.",
                  "The unitary executive theory applies only during wartime and national emergencies."]),
     "The unitary executive theory argues that Article II's vesting of 'executive Power' in the President means that all executive authority ultimately resides in the President alone. This theory supports broad presidential power to remove executive officers, direct agency decision-making, and interpret laws independently of Congress and the courts. Critics argue it undermines congressional oversight and the independent agencies created by Congress. The theory has influenced debates about presidential control over regulatory agencies, executive privilege, and the scope of presidential authority in national security matters."),

    # Hard: deeper federalism (5)
    (2, "Federalism", "hard",
     "What is 'preemption,' and how does it affect state law?",
     "Preemption is the doctrine that when federal and state law conflict, federal law prevails under the Supremacy Clause; it can be express (stated in federal law) or implied (from federal intent).",
     json.dumps(["Preemption means that state laws always override federal laws in all circumstances.",
                  "Preemption only applies to criminal law and has no effect on civil regulations.",
                  "Preemption was eliminated by the Tenth Amendment and no longer exists in American law."]),
     "Federal preemption occurs when Congress, acting within its constitutional authority, enacts legislation that overrides conflicting state law. Express preemption occurs when federal law explicitly states that it preempts state law. Implied preemption occurs when federal law is so comprehensive that it occupies an entire field (field preemption) or when state law conflicts with federal objectives (conflict preemption). The Supremacy Clause provides the constitutional basis: when federal and state law conflict, federal law prevails. Preemption analysis often requires courts to determine congressional intent."),

    (2, "Federalism", "hard",
     "What was the significance of McCulloch v Maryland (1819) for American federalism?",
     "It established that states cannot tax federal institutions and broadly interpreted Congress's powers under the Necessary and Proper Clause, strengthening federal authority.",
     json.dumps(["It established that states can tax federal institutions without limitation.",
                  "It had no lasting significance; the decision was quickly overturned.",
                  "It eliminated state sovereignty and established complete federal control over all government functions."]),
     "McCulloch v Maryland (1819) is one of the most important Supreme Court decisions in American federalism. The Court held that (1) Congress has implied powers under the Necessary and Proper Clause to create a national bank, even though the Constitution does not explicitly mention banks, and (2) states cannot tax federal institutions because 'the power to tax is the power to destroy.' Chief Justice Marshall's opinion established the principle of implied powers and national supremacy, significantly strengthening the federal government relative to the states."),

    (2, "Federalism", "hard",
     "How did the New Deal era transform American federalism, and what constitutional principle was affected?",
     "The New Deal era shifted federalism from dual to cooperative by expanding Congress's Commerce Clause power, allowing federal regulation of virtually any economic activity.",
     json.dumps(["The New Deal era eliminated federalism entirely and established a unitary national government.",
                  "The New Deal had no effect on federalism; the states maintained all their traditional powers.",
                  "The New Deal era strengthened dual federalism by clearly separating federal and state powers."]),
     "The New Deal era (1933-1939) fundamentally transformed American federalism from dual federalism (where federal and state governments operated in separate spheres) to cooperative federalism (where they share responsibilities). The key constitutional shift was the Supreme Court's dramatic expansion of Congress's Commerce Clause power. After initially striking down New Deal programs, the Court reversed course and adopted a broad interpretation of interstate commerce that allowed federal regulation of virtually any economic activity. This enabled the modern regulatory state and federal involvement in areas previously reserved to the states."),

    (2, "Federalism", "hard",
     "What is 'new federalism' (devolution), and how does it differ from cooperative federalism?",
     "New federalism seeks to return power to the states through block grants, unfunded mandates reform, and Supreme Court rulings that limit federal power over states.",
     json.dumps(["New federalism and cooperative federalism are identical concepts with different names.",
                  "New federalism gives the federal government more power over states than cooperative federalism.",
                  "New federalism eliminates state governments entirely and creates a single national government."]),
     "New federalism (also called devolution) is a political and judicial movement since the 1970s that seeks to shift power and responsibility from the federal government back to the states. It differs from cooperative federalism by emphasizing state autonomy rather than federal-state partnership. Key elements include: converting categorical grants (tied to specific federal requirements) into block grants (with broader state discretion), reforming unfunded mandates (requiring the federal government to fund requirements it imposes on states), and Supreme Court decisions that limit federal power over states (like Printz v United States and Lopez v United States)."),

    (2, "Federalism", "hard",
     "In United States v Lopez (1995), what did the Supreme Court rule about the Commerce Clause, and why was it significant?",
     "The Court ruled that the Gun-Free School Zones Act exceeded Congress's Commerce Clause power, marking the first time since the New Deal that the Court limited Congress's commerce power.",
     json.dumps(["The Court upheld unlimited congressional power under the Commerce Clause without any restrictions.",
                  "The Court ruled that the Commerce Clause was unconstitutional and should be removed from the Constitution.",
                  "The Court held that the Commerce Clause only applies to international trade, not interstate commerce."]),
     "United States v Lopez (1995) was a landmark decision in which the Supreme Court struck down the Gun-Free School Zones Act as exceeding Congress's Commerce Clause power. Chief Justice Rehnquist's majority opinion held that the law did not regulate a commercial activity, did not contain a jurisdictional element to ensure it affected interstate commerce, and would give Congress a general police power — something the Constitution reserves to the states. This was the first time since 1937 that the Court invalidated a federal law as exceeding Commerce Clause authority, signaling a potential shift in federalism jurisprudence."),

    # Medium: remaining gaps (15)
    (2, "Amendment process", "medium",
     "How many times has the Constitution been amended?",
     "Twenty-seven times.",
     json.dumps(["Ten times, with the Bill of Rights being the last amendment.",
                  "Fifty times, with the most recent amendment passed in 2020.",
                  "One hundred times, with amendments added every decade."]),
     "The Constitution has been amended 27 times. The first ten amendments (the Bill of Rights) were ratified in 1791. The most recent amendment is the Twenty-Seventh Amendment, ratified in 1992, which prohibits Congress from giving itself a pay raise that takes effect before the next election. Remarkably, this amendment was originally proposed by James Madison in 1789 as part of the original Bill of Rights package but was not ratified by the required number of states until a grassroots campaign succeeded in the late 20th century."),

    (2, "Amendment process", "medium",
     "Which amendment was ratified most recently, and how long did it take?",
     "The Twenty-Seventh Amendment (congressional pay), ratified in 1992 — 202 years and 7 months after it was proposed in 1789.",
     json.dumps(["The Twenty-Sixth Amendment (voting age 18), ratified in 1971 after 2 years.",
                  "The First Amendment (free speech), ratified in 1791 after 3 months.",
                  "The Second Amendment (right to bear arms), ratified in 1791 after 5 years."]),
     "The Twenty-Seventh Amendment, ratified on May 7, 1992, holds the record for the longest ratification process in American history — 202 years, 7 months, and 10 days. Originally proposed by James Madison in 1789 as one of the amendments sent to the states for ratification, it was not adopted at the time because it did not receive the required number of state ratifications. In the 1980s, a University of Texas student named Gregory Watson discovered the unratified amendment and began a letter-writing campaign that eventually led to its ratification."),

    (2, "Amendment process", "hard",
     "What is a 'constitutional convention' for proposing amendments, and why has one never been called?",
     "Two-thirds of state legislatures can call a convention to propose amendments, but none has ever been called due to fears about the scope of such a convention and lack of rules governing its process.",
     json.dumps(["A constitutional convention has been called three times and resulted in the Bill of Rights, the Reconstruction Amendments, and the New Deal Amendments.",
                  "The Constitution prohibits constitutional conventions and requires all amendments to come from Congress.",
                  "A constitutional convention requires unanimous consent of all states, making it impossible to achieve."]),
     "Article V provides two methods for proposing amendments: Congress (two-thirds of both houses) or a constitutional convention called by two-thirds of state legislatures. Although the convention method has never been used, it came close during the 20th century when 34 states (the required two-thirds) applied for a convention to propose a balanced budget amendment. However, concerns about a 'runaway convention' that could rewrite the entire Constitution, combined with uncertainty about how such a convention would operate (no rules exist in the Constitution or federal law), have prevented the convention method from ever being triggered."),

    (2, "Legislative branch", "medium",
     "What is a pocket veto, and when can a President use it?",
     "A pocket veto occurs when the President does not sign a bill within 10 days and Congress has adjourned, preventing the bill from becoming law.",
     json.dumps(["A pocket veto allows the President to veto a bill at any time after it has been signed into law.",
                  "A pocket veto requires the approval of both houses of Congress and the Supreme Court.",
                  "A pocket veto is a type of veto that applies only to bills related to the federal budget."]),
     "A pocket veto occurs when the President receives a bill but does not sign it within the 10-day period allowed by the Constitution, AND Congress has adjourned during that period. Under these circumstances, the bill does not become law because the President cannot return it to Congress. This differs from a regular veto, where the President returns the bill to Congress with objections, giving Congress the opportunity to override the veto with a two-thirds vote. The pocket veto is absolute — Congress cannot override it because it has already adjourned."),

    (2, "Legislative branch", "medium",
     "What is the purpose of congressional committees, and how do they influence legislation?",
     "Committees specialize in specific policy areas, conduct hearings, amend bills, and determine which legislation reaches the full chamber for a vote.",
     json.dumps(["Committees are ceremonial bodies with no real power over legislation.",
                  "Committees only exist to organize social events for members of Congress.",
                  "Committees are appointed by the President to oversee congressional activities."]),
     "Congressional committees are the workhorses of the legislative process. Standing committees specialize in specific policy areas (like the Armed Services Committee, Ways and Means Committee, or Judiciary Committee). They conduct hearings, gather information, amend legislation, and decide which bills advance to the full chamber. Most bills die in committee without ever reaching the floor. The committee system allows Congress to divide its enormous workload among smaller groups of members who develop expertise in specific policy areas. Committee chairs have significant power to set agendas and influence outcomes."),

    (2, "Executive branch", "medium",
     "What is the President's role as Commander in Chief, and what limits does Congress place on this power?",
     "The President commands the armed forces but Congress has the power to declare war, raise and fund armies, and regulate the military through legislation.",
     json.dumps(["The President has unlimited military authority and can declare war without congressional approval.",
                  "Congress has complete military authority and the President has no role in military decisions.",
                  "The Commander in Chief role is purely ceremonial with no actual authority over military operations."]),
     "Article II designates the President as Commander in Chief of the armed forces, giving the President authority over military operations, strategy, and troop deployments. However, Article I gives Congress the power to declare war, raise and support armies, provide and maintain a navy, and make rules governing the armed forces. This division of war powers has been the source of ongoing tension, especially since the passage of the War Powers Resolution (1973), which requires the President to notify Congress within 48 hours of deploying troops and limits military engagements to 60 days without congressional authorization."),

    (2, "Executive branch", "medium",
     "What is the role of the President's cabinet, and how are cabinet members selected?",
     "Cabinet members head the 15 executive departments and advise the President; they are nominated by the President and confirmed by the Senate.",
     json.dumps(["Cabinet members are elected directly by the American people in national elections.",
                  "Cabinet members are appointed by the Supreme Court and serve for life.",
                  "The cabinet is a ceremonial body with no advisory role in government policy."]),
     "The President's cabinet consists of the heads of the 15 executive departments (State, Treasury, Defense, Attorney General, Interior, Agriculture, Commerce, Labor, HHS, HUD, Transportation, Energy, Education, VA, and Homeland Security) plus other senior officials the President may designate. Cabinet members serve at the pleasure of the President and can be dismissed at any time. They advise the President on policy matters within their departments' areas of responsibility. The cabinet meets regularly, though its role and influence vary significantly depending on each President's management style."),

    (2, "Judicial branch", "medium",
     "What is the difference between a strict constructionist and a loose constructionist approach to constitutional interpretation?",
     "Strict constructionists interpret the Constitution narrowly based on its literal text; loose constructionists interpret it more broadly, considering the document's purpose and contemporary context.",
     json.dumps(["There is no difference; both terms describe the same judicial philosophy.",
                  "Strict constructionists believe the Constitution should be rewritten every ten years.",
                  "Loose constructionists believe only the President can interpret the Constitution."]),
     "Strict constructionism interprets the Constitution by focusing on the literal text and original meaning of its provisions, giving the federal government only those powers explicitly stated. Loose constructionism (or broad constructionism) interprets the Constitution more flexibly, considering its purposes, the Framers' intent, and contemporary circumstances. The tension between these approaches has shaped American constitutional history. Hamilton and the Federalists favored loose construction, while Jefferson and the Democratic-Republicans favored strict construction — though both sides switched positions when politically convenient."),

    (2, "Judicial branch", "medium",
     "What is the significance of a Supreme Court dissenting opinion?",
     "Dissenting opinions record disagreement with the majority, may influence future courts to overturn precedent, and provide alternative legal reasoning.",
     json.dumps(["Dissenting opinions have no legal effect and are never read by anyone.",
                  "Dissenting opinions automatically become law after five years.",
                  "Dissenting opinions can only be written by the Chief Justice."]),
     "Dissenting opinions are written by justices who disagree with the majority's decision. While they do not carry the force of law, dissents serve several important functions. They provide an alternative legal analysis that may persuade future courts to overturn or limit the majority decision. Justice Harlan's dissent in Plessy v Ferguson became the foundation for Brown v Board of Education 58 years later. Dissents also highlight weaknesses in the majority's reasoning and may influence public opinion and legal scholarship. The right to dissent is considered essential to the integrity of the judicial process."),

    (2, "Judicial branch", "hard",
     "What is stare decisis, and when might the Supreme Court choose to overturn precedent?",
     "Stare decisis is the principle of following established precedent; the Court may overturn precedent when the precedent proves unworkable, was wrongly decided, or when societal conditions have fundamentally changed.",
     json.dumps(["Stare decisis requires the Court to follow every precedent forever without exception.",
                  "Stare decisis means the Court must always overturn precedent every time a new justice joins the Court.",
                  "Stare decisis applies only to state courts, not to the federal judiciary."]),
     "Stare decisis (Latin for 'to stand by things decided') is the legal principle that courts should follow established precedents when deciding similar cases. This promotes stability, predictability, and fairness in the law. However, the Supreme Court can and does overturn precedent when conditions warrant it. Factors the Court considers include whether the precedent has proven unworkable, whether it was poorly reasoned from the start, whether it has been eroded by subsequent decisions, and whether changed circumstances make the precedent obsolete. Notable precedent overrules include Brown v Board (overturning Plessy) and Dobbs v Jackson (overturning Roe v Wade)."),

    (2, "Checks and balances", "medium",
     "What are three ways the President can check the legislative branch?",
     "The veto, calling special sessions of Congress, and enforcing (or choosing not to enforce) laws passed by Congress.",
     json.dumps(["The President can dissolve Congress, veto constitutional amendments, and appoint state governors.",
                  "The President can rewrite laws passed by Congress, create new taxes, and declare treaties without Senate approval.",
                  "The President has no checks on the legislative branch; Congress is completely independent."]),
     "The President has several constitutional checks on the legislative branch. The veto power allows the President to reject bills passed by Congress (Congress can override with two-thirds vote). The President can call special sessions of Congress in emergencies. Through the appointment power, the President influences the judiciary that interprets laws. The President's role as Commander in Chief provides a check on Congress's war powers. Additionally, the President's power to issue executive orders and the discretion in how vigorously to enforce laws (prosecutorial discretion) give the President significant influence over how congressional legislation is implemented."),

    (2, "Checks and balances", "medium",
     "How does the legislative branch check the judicial branch?",
     "Through Senate confirmation of judges, the power to create and restructure lower courts, impeachment, and the power to amend the Constitution to override judicial decisions.",
     json.dumps(["Congress has no checks on the judiciary; the courts are completely independent.",
                  "Congress can only check the judiciary by voting to increase judges' salaries.",
                  "The judiciary is checked exclusively by the executive branch, not the legislature."]),
     "Congress exercises several checks on the judicial branch. The Senate confirms all federal judges, giving the legislative branch influence over judicial appointments. Congress has the power to create and abolish lower federal courts and determine their jurisdiction. The House can impeach and the Senate can convict federal judges for 'high crimes and misdemeanors.' Congress can also pass new laws or constitutional amendments to override Supreme Court decisions. Additionally, Congress controls the judiciary's budget and can use the power of the purse to influence court operations."),

    (2, "Checks and balances", "hard",
     "What is the 'veto override' process, and how often has it been successfully used against a President's veto?",
     "Congress can override a veto with a two-thirds vote in both chambers; this has been used successfully about 7% of the time (111 overrides out of approximately 2,500 vetoes).",
     json.dumps(["A veto override requires only a simple majority in one chamber and has been used thousands of times.",
                  "Veto overrides have never been successful in American history; the President's veto is absolute.",
                  "A veto override requires approval from the Supreme Court and has been used only twice."]),
     "Article I, Section 7 provides that if the President vetoes a bill, Congress can override the veto by a two-thirds vote in both the House and Senate. This is one of the most significant checks the legislative branch has on the executive. Historically, Congress has overridden approximately 7% of all presidential vetoes (about 111 out of roughly 2,500 total vetoes). Override success depends on the size of the President's opposition in Congress and the political stakes of the vetoed legislation. Override attempts that fall short of two-thirds by just a few votes are relatively common."),

    (2, "Key amendments", "medium",
     "What did the Sixteenth Amendment authorize, and why was it necessary?",
     "It authorized a federal income tax; it was necessary because the Supreme Court had ruled in Pollock v Farmers' Loan (1895) that income taxes were direct taxes requiring apportionment among states.",
     json.dumps(["It authorized the federal government to ban alcohol; it was necessary because of the temperance movement.",
                  "It authorized women's suffrage; it was necessary because the original Constitution restricted voting to men.",
                  "It authorized the direct election of senators; it was necessary because state legislatures were corrupt."]),
     "The Sixteenth Amendment, ratified in 1913, gave Congress the power to 'lay and collect taxes on incomes, from whatever source derived, without apportionment among the several States.' This was necessary because in Pollock v Farmers' Loan and Trust Co. (1895), the Supreme Court struck down the federal income tax enacted in 1894, ruling that taxes on income from property were direct taxes requiring apportionment among the states by population — a requirement that made a practical income tax impossible. The Sixteenth Amendment resolved this by explicitly authorizing income taxes without apportionment."),

    (2, "Key amendments", "medium",
     "What did the Seventeenth Amendment change about how U.S. Senators are selected?",
     "It required direct election of Senators by the voters of each state, replacing the previous system of selection by state legislatures.",
     json.dumps(["It changed the term length of Senators from six years to four years.",
                  "It eliminated the Senate entirely and transferred its powers to the House.",
                  "It required Senators to be appointed by the President instead of elected."]),
     "The Seventeenth Amendment, ratified in 1913, established the direct election of U.S. Senators by popular vote in each state. Previously, Article I, Section 3 provided that Senators would be chosen by state legislatures. The amendment was driven by Progressive Era reformers who argued that state legislative selection of Senators was corrupt, undemocratic, and led to deadlocks when legislatures couldn't agree on a choice. The amendment also provided a procedure for governors to fill Senate vacancies by appointment until a special election could be held."),

    (2, "Key amendments", "hard",
     "What is the significance of the Fourteenth Amendment's Equal Protection Clause in modern constitutional law?",
     "The Equal Protection Clause has become the primary constitutional tool for combating discrimination, applied to race, gender, sexual orientation, and other classifications with varying levels of scrutiny.",
     json.dumps(["The Equal Protection Clause only applies to taxation and has no relevance to civil rights.",
                  "The Equal Protection Clause was repealed by the Twenty-Fourth Amendment and no longer exists.",
                  "The Equal Protection Clause only protects the rights of property owners and business interests."]),
     "The Fourteenth Amendment's Equal Protection Clause — 'No State shall... deny to any person within its jurisdiction the equal protection of the laws' — has become the constitutional foundation for modern civil rights law. The Supreme Court applies different levels of scrutiny to laws that classify people: strict scrutiny for race-based classifications (government must show a compelling interest), intermediate scrutiny for gender-based classifications (substantial interest), and rational basis review for most other classifications. The Clause has been used in landmark cases including Brown v Board of Education (school desegregation), Loving v Virginia (interracial marriage), and Obergefell v Hodges (same-sex marriage)."),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
for q in questions:
    cur.execute(
        "INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation) VALUES (?,?,?,?,?,?,?)",
        q
    )
conn.commit()
print(f"Inserted {len(questions)} D2 questions")
conn.close()
