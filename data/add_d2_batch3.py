#!/usr/bin/env python3
"""Add D2 questions batch 3: more state/local gov, deeper federalism, executive powers, amendment details."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Deeper Federalism (5)
    (2, "Federalism", "hard",
     "What is the difference between dual federalism and cooperative federalism?",
     "Dual federalism maintains strict separation between federal and state powers; cooperative federalism blends federal and state responsibilities with shared costs and administration.",
     json.dumps(["Dual federalism means states have no power; cooperative federalism means states have all power.",
                  "Dual federalism was created by the New Deal; cooperative federalism existed before the Constitution.",
                  "There is no difference; they are different names for the same concept."]),
     "Dual federalism (also called 'layer cake federalism') dominated from the Constitution's ratification until the New Deal era. Under this model, federal and state governments operate in separate spheres with clearly defined powers. Cooperative federalism ('marble cake federalism') emerged during the New Deal and expanded after World War II, characterized by shared powers, shared costs, and shared administration of programs. Federal grants to states, federal-state partnerships, and concurrent powers all reflect cooperative federalism."),

    (2, "Federalism", "medium",
     "What is a concurrent power, and give two examples?",
     "Concurrent powers are powers shared by both federal and state governments, such as the power to tax and the power to establish courts.",
     json.dumps(["Concurrent powers are powers that only the federal government can exercise, such as declaring war and printing money.",
                  "Concurrent powers are powers reserved exclusively for state governments, such as conducting elections.",
                  "Concurrent powers are powers that neither government can exercise without a constitutional amendment."]),
     "Concurrent powers are powers that both the federal government and state governments can exercise simultaneously. Examples include the power to tax, borrow money, establish courts, make and enforce laws, and charter banks. When federal and state laws conflict on concurrent powers, the Supremacy Clause (Article VI) establishes that federal law prevails. Concurrent powers are essential to cooperative federalism, allowing both levels of government to address shared problems like crime, education, and transportation."),

    (2, "Federalism", "easy",
     "What is an exclusive power of the federal government?",
     "A power that only the federal government can exercise, such as declaring war, printing money, or regulating interstate commerce.",
     json.dumps(["A power that all levels of government share equally without restriction.",
                  "A power that only state governments can exercise in their own territories.",
                  "A power that is reserved for the President alone without congressional approval."]),
     "Exclusive powers are powers granted solely to the federal government by the Constitution. Examples include declaring war, coining money, regulating interstate and foreign commerce, conducting foreign relations, maintaining armed forces, and establishing immigration rules. States cannot exercise these powers. The Constitution also includes powers prohibited to states (Article I, Section 10), such as making treaties, coining money, or granting titles of nobility, further reinforcing the distinction between federal and state authority."),

    (2, "Federalism", "medium",
     "What is the Supremacy Clause and why is it important to federalism?",
     "The Supremacy Clause (Article VI) establishes that the Constitution and federal laws are the supreme law of the land, overriding conflicting state laws.",
     json.dumps(["The Supremacy Clause gives state governments the power to override federal laws they disagree with.",
                  "The Supremacy Clause establishes that the President is supreme over all other branches of government.",
                  "The Supremacy Clause requires all states to have identical laws on every subject."]),
     "Article VI, Clause 2 of the Constitution states: 'This Constitution, and the Laws of the United States which shall be made in Pursuance thereof... shall be the supreme Law of the Land.' This Supremacy Clause resolves conflicts between federal and state law in favor of federal law. However, the federal government can only exercise powers delegated by the Constitution — it cannot compel states to pass specific laws (per the anti-commandeering doctrine from Printz v United States, 1997). The Supremacy Clause is the constitutional foundation of American federalism."),

    (2, "Federalism", "hard",
     "What is the anti-commandeering doctrine, and which Supreme Court case established it?",
     "The anti-commandeering doctrine prohibits the federal government from compelling state governments to enforce federal law; established in Printz v United States (1997).",
     json.dumps(["The anti-commandeering doctrine requires states to enforce all federal laws; it was established in McCulloch v Maryland.",
                  "The anti-commandeering doctrine allows the President to take direct control of state National Guard units; it was established in Marbury v Madison.",
                  "The anti-commandeering doctrine was proposed but never actually adopted by the Supreme Court."]),
     "The anti-commandeering doctrine holds that the federal government cannot compel state governments to enforce or administer federal regulatory programs. Established in Printz v United States (1997) and reinforced in New York v United States (1992), the doctrine rests on the principle that the Constitution creates a dual sovereignty between federal and state governments. While the Supremacy Clause makes federal law supreme, it does not allow the federal government to conscript state executive officials to implement federal policy."),

    # Deeper Executive branch (5)
    (2, "Executive branch", "medium",
     "What are the formal qualifications to become President of the United States?",
     "Must be a natural-born citizen, at least 35 years old, and a resident of the United States for at least 14 years.",
     json.dumps(["Must be a natural-born citizen, at least 40 years old, and have served in the military.",
                  "Must be born in the United States, have a law degree, and have been a governor or senator.",
                  "Must be a citizen for at least 20 years, at least 30 years old, and own property."]),
     "Article II, Section 1 of the Constitution establishes three qualifications for the presidency: natural-born citizenship, minimum age of 35, and 14 years of U.S. residency. These are the only constitutional requirements — there is no requirement for military service, prior government experience, education, or property ownership. The natural-born citizen clause has been the subject of debate, but has been interpreted to include anyone born a U.S. citizen, whether on American soil or abroad to U.S. citizen parents."),

    (2, "Executive branch", "medium",
     "What is the Electoral College and how does it work?",
     "A body of electors equal to each state's congressional delegation that formally elects the President; 270 electoral votes are needed to win.",
     json.dumps(["A direct popular vote system where the candidate with the most individual votes nationwide wins the presidency.",
                  "A committee of members of Congress who choose the President by majority vote.",
                  "A system where state governors vote to determine the next President."]),
     "The Electoral College is the constitutional system for electing the President (Article II, Section 1, modified by the Twelfth Amendment). Each state has electors equal to its total congressional delegation (House + Senate seats), plus three for Washington, D.C. Most states use a winner-take-all system where the candidate who wins the state's popular vote receives all its electoral votes. A candidate needs 270 of 538 electoral votes to win. If no candidate reaches 270, the House of Representatives chooses the President."),

    (2, "Executive branch", "hard",
     "What is executive privilege, and what limits does the Supreme Court have placed on it?",
     "Executive privilege is the President's right to withhold information from other branches; the Court ruled in US v Nixon (1974) that it is not absolute and must yield to judicial needs.",
     json.dumps(["Executive privilege is unlimited; the President can withhold any information for any reason without exception.",
                  "Executive privilege does not exist; the President must disclose all information to Congress upon request.",
                  "Executive privilege only applies to military matters and has no application to domestic policy."]),
     "Executive privilege is the constitutional principle that the President can withhold certain communications from Congress and the courts to protect the confidentiality of executive branch deliberations. In United States v Nixon (1974), the Supreme Court unanimously ruled that while executive privilege exists, it is not absolute. When the evidence is needed for the fair administration of criminal justice, the privilege must yield. This case forced Nixon to surrender the Watergate tapes, leading to his resignation."),

    (2, "Executive branch", "easy",
     "What is the primary role of the Vice President as defined in the Constitution?",
     "To serve as President of the Senate and to assume the presidency if the President dies, resigns, or is removed from office.",
     json.dumps(["To manage the day-to-day operations of the executive branch departments.",
                  "To serve as the chief justice of the Supreme Court when a vacancy occurs.",
                  "To lead the military as Commander in Chief when the President is unavailable."]),
     "The Vice President has two constitutional roles: serving as President of the Senate (with a tie-breaking vote) and succeeding the President if the office becomes vacant. Beyond these, the Vice President's role is largely determined by the President — modern Vice Presidents often serve as key advisors and take on significant policy responsibilities. The Vice President's limited constitutional role reflects the Founders' initial view of the office as a secondary position, though modern vice presidencies have grown significantly in importance."),

    (2, "Executive branch", "hard",
     "What is the Twenty-Fifth Amendment, and when has it been invoked?",
     "The Twenty-Fifth Amendment clarifies presidential succession, vice presidential vacancies, and presidential disability; it was invoked when Ford became VP and when both Reagan and Biden temporarily transferred power.",
     json.dumps(["The Twenty-Fifth Amendment limits the President to two terms in office.",
                  "The Twenty-Fifth Amendment abolishes the Electoral College in favor of direct popular vote.",
                  "The Twenty-Fifth Amendment gives Congress the power to remove federal judges."]),
     "The Twenty-Fifth Amendment (1967) addresses four key issues: (1) the Vice President becomes President if the President dies, resigns, or is removed; (2) the President nominates a new Vice President, confirmed by Congress (used when Ford replaced Agnew, then Rockefeller replaced Ford); (3) the President can temporarily transfer power to the Vice President by declaring inability to serve (used by Reagan and Bush during medical procedures); (4) the Vice President and Cabinet can declare the President unable to serve, with Congress having the final say."),

    # Deeper Legislative branch (5)
    (2, "Legislative branch", "medium",
     "What is the difference between the House of Representatives and the Senate in terms of representation?",
     "House seats are apportioned by state population (435 total), while each state has exactly two Senators regardless of population.",
     json.dumps(["Both chambers have equal representation; every state has the same number of representatives in each.",
                  "The House has two representatives per state; the Senate has representation based on population.",
                  "Representation in both chambers is determined solely by each state's land area."]),
     "The Great Compromise of 1787 created a bicameral Congress with two different methods of representation. The House of Representatives is based on proportional representation — larger states have more representatives, currently fixed at 435 seats apportioned by state population. The Senate provides equal representation — each state has exactly two Senators, regardless of population. This dual structure balances the interests of large and small states and was a crucial compromise that made the Constitution possible."),

    (2, "Legislative branch", "medium",
     "What are the exclusive powers of the Senate that the House does not have?",
     "The Senate has the exclusive power to confirm presidential appointments, ratify treaties, and try impeachment cases.",
     json.dumps(["The Senate exclusively has the power to initiate revenue bills and impeach federal officials.",
                  "The Senate exclusively has the power to declare war and appoint federal judges.",
                  "The Senate has no exclusive powers; both chambers share identical constitutional authority."]),
     "The Constitution grants the Senate several exclusive powers. Article II requires Senate confirmation of presidential appointments (cabinet secretaries, federal judges, ambassadors). The Senate also has the sole power to ratify treaties negotiated by the President (two-thirds vote required). In impeachment proceedings, while the House has the sole power to impeach (bring charges), the Senate has the sole power to try impeachments, with the Chief Justice presiding when the President is tried. A two-thirds vote is required for conviction."),

    (2, "Legislative branch", "easy",
     "How many members are in the House of Representatives and the Senate?",
     "The House has 435 voting members; the Senate has 100 members (two per state).",
     json.dumps(["The House has 100 members; the Senate has 435 members.",
                  "Both chambers have 535 members each.",
                  "The House has 50 members; the Senate has 435 members."]),
     "The House of Representatives has 435 voting members, apportioned among the states based on population, with each state guaranteed at least one representative. Representatives serve two-year terms. The Senate has 100 members — two from each of the 50 states — serving six-year terms with staggered elections (approximately one-third of the Senate is elected every two years). The Vice President serves as President of the Senate but only votes to break ties."),

    (2, "Legislative branch", "medium",
     "What is a filibuster, and how can it be ended?",
     "A filibuster is a tactic to delay or block a vote by extending debate; it can be ended by a cloture vote of 60 senators.",
     json.dumps(["A filibuster is a rule that automatically passes a bill if it receives majority support.",
                  "A filibuster is when the President veto overrides a congressional vote; it requires a two-thirds majority to end.",
                  "A filibuster is a type of committee hearing that all senators must attend."]),
     "A filibuster is a Senate tactic where a senator or group of senators extends debate to delay or block a vote on a bill or nomination. Because Senate rules generally allow unlimited debate, a single senator can potentially delay legislation indefinitely. Filibusters can be ended by invoking 'cloture,' which requires the votes of 60 out of 100 senators. The filibuster is a feature unique to the Senate — the House has strict time limits on debate. Critics argue it gives a minority of senators excessive power to block legislation."),

    (2, "Legislative branch", "hard",
     "What is the 'necessary and proper clause' and why is it sometimes called the 'elastic clause'?",
     "The Necessary and Proper Clause (Article I, Section 8) gives Congress the power to make laws needed to carry out its enumerated powers; it is 'elastic' because it has been interpreted broadly to expand congressional authority.",
     json.dumps(["The Necessary and Proper Clause gives the President unlimited power during national emergencies.",
                  "The clause requires all laws to be 'proper' in a moral sense before they can be passed.",
                  "The clause was added by the Twenty-First Amendment and applies only to state governments."]),
     "The Necessary and Proper Clause (Article I, Section 8, Clause 18) states that Congress has the power 'to make all Laws which shall be necessary and proper for carrying into Execution the foregoing Powers.' This clause has been called the 'elastic clause' because it has been interpreted expansively to give Congress broad implied powers beyond those explicitly listed. In McCulloch v Maryland (1819), Chief Justice Marshall ruled that 'necessary' means 'convenient or useful,' not absolutely indispensable, allowing Congress to create a national bank even though the Constitution does not explicitly mention banks."),

    # Deeper Judicial branch (5)
    (2, "Judicial branch", "medium",
     "How many Supreme Court justices are there, and how long do they serve?",
     "Nine justices serve on the Supreme Court; they serve for life ('during good behavior') unless they resign, retire, or are impeached.",
     json.dumps(["Seven justices serve for ten-year terms that can be renewed once.",
                  "Eleven justices serve for life with mandatory retirement at age 75.",
                  "Fifteen justices serve for fifteen-year terms."]),
     "The Supreme Court consists of nine justices: one Chief Justice and eight Associate Justices. The number has changed six times throughout American history, ranging from five to ten, but has been fixed at nine since 1869. Justices are appointed by the President and confirmed by the Senate. They serve 'during good behavior' (effectively for life) as specified in Article III, meaning they can only be removed through impeachment by the House and conviction by the Senate. This lifetime appointment is designed to insulate justices from political pressure."),

    (2, "Judicial branch", "hard",
     "What is judicial review, and how was it established?",
     "Judicial review is the power of courts to determine whether laws are constitutional; it was established by the Supreme Court in Marbury v Madison (1803).",
     json.dumps(["Judicial review is the President's power to reject Supreme Court decisions; it was established by the Constitution's original text.",
                  "Judicial review is Congress's power to override judicial decisions by majority vote; it was established by the First Amendment.",
                  "Judicial review is the process by which the Senate reviews judicial nominees; it was established by the Judiciary Act of 1789."]),
     "Judicial review is the power of federal courts to declare legislative and executive acts unconstitutional. Chief Justice John Marshall established this principle in Marbury v Madison (1803), ruling that 'it is emphatically the province and duty of the judicial department to say what the law is.' While judicial review is not explicitly mentioned in the Constitution, it has become a cornerstone of American constitutional law. Marshall reasoned that the Constitution is 'a superior, paramount law' that judges are bound to enforce, and that laws conflicting with the Constitution must yield."),

    (2, "Judicial branch", "medium",
     "What is the difference between original jurisdiction and appellate jurisdiction?",
     "Original jurisdiction means a court hears a case first; appellate jurisdiction means a court reviews a lower court's decision.",
     json.dumps(["Original jurisdiction applies only to criminal cases; appellate jurisdiction applies only to civil cases.",
                  "Original jurisdiction means the Supreme Court has the final say; appellate jurisdiction means a lower court decides.",
                  "There is no difference; both terms refer to the same type of jurisdiction."]),
     "Original jurisdiction is the authority of a court to hear a case first, as a trial court. The Supreme Court's original jurisdiction is limited to cases involving ambassadors, public ministers, consuls, and cases where a state is a party (Article III, Section 2). Appellate jurisdiction is the authority to review decisions of lower courts. The vast majority of Supreme Court cases come through appellate jurisdiction — the Court reviews decisions of federal appeals courts and state supreme courts. The distinction is fundamental to the American judicial system's structure."),

    (2, "Judicial branch", "easy",
     "What are the three levels of the federal court system?",
     "District courts (trial level), Courts of Appeals (intermediate), and the Supreme Court (highest).",
     json.dumps(["State courts, federal courts, and international courts.",
                  "The Supreme Court, the Cabinet, and the Electoral College.",
                  "Military courts, tax courts, and bankruptcy courts."]),
     "The federal court system has three levels. At the bottom are 94 district courts (trial courts), which hear federal cases including civil and criminal matters. In the middle are 13 Courts of Appeals (also called circuit courts), which review decisions of district courts within their geographic circuits. At the top is the Supreme Court, which has discretionary appellate jurisdiction over both federal and state court decisions involving federal questions. This hierarchical structure allows for review and correction of lower court decisions."),

    (2, "Judicial branch", "medium",
     "How does a case reach the Supreme Court for review?",
     "Most commonly through a writ of certiorari, which the Court grants when at least four justices agree to hear the case (the 'Rule of Four').",
     json.dumps(["Any citizen can directly file a case with the Supreme Court without going through lower courts.",
                  "The President can order the Supreme Court to hear any case of national importance.",
                  "Cases automatically reach the Supreme Court after being decided by any state court."]),
     "The Supreme Court receives approximately 7,000-8,000 petitions per term but hears only about 70-80 cases. Most cases reach the Court through a petition for a writ of certiorari, asking the Court to review a lower court's decision. The Court grants cert when at least four of the nine justices agree to hear the case (the 'Rule of Four'). The Court tends to grant cert when there is a circuit split (different appeals courts reaching different conclusions on the same issue), when a case involves a significant federal question, or when a lower court's decision conflicts with existing Supreme Court precedent."),
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
