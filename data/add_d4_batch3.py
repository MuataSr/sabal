#!/usr/bin/env python3
"""Add D4 questions batch 3: Mapp v Ohio, Roe v Wade, executive orders, New Deal/Great Society, deeper case analysis."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Mapp v Ohio (5)
    (4, "Mapp v Ohio", "easy",
     "What did the Supreme Court rule in Mapp v Ohio (1961)?",
     "Evidence obtained through unreasonable searches and seizures cannot be used in state courts (the exclusionary rule applies to states).",
     json.dumps(["Police can search any home without a warrant if they suspect a crime has been committed.",
                  "Only federal courts must exclude illegally obtained evidence; state courts can use it freely.",
                  "The Fourth Amendment does not apply to searches of private residences."]),
     "Mapp v Ohio (1961) extended the exclusionary rule — which prohibits the use of illegally obtained evidence in criminal trials — to all state courts through the Fourteenth Amendment's Due Process Clause. Before Mapp, the exclusionary rule applied only to federal courts (from Weeks v United States, 1914). Police had searched Dollree Mapp's home without a proper warrant and found obscene materials. The Supreme Court overturned her conviction, ruling that all evidence obtained by searches and seizures in violation of the Constitution is inadmissible in state courts."),

    (4, "Mapp v Ohio", "medium",
     "What constitutional amendment was at issue in Mapp v Ohio?",
     "The Fourth Amendment's protection against unreasonable searches and seizures.",
     json.dumps(["The Second Amendment's right to bear arms.",
                  "The Eighth Amendment's prohibition on excessive bail.",
                  "The Tenth Amendment's reservation of powers to the states."]),
     "Mapp v Ohio centered on the Fourth Amendment, which states: 'The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures, shall not be violated, and no Warrants shall issue, but upon probable cause.' The Court ruled that the Fourth Amendment's exclusionary rule — developed for federal courts in Weeks v United States (1914) — must also apply to state courts through the Fourteenth Amendment's Due Process Clause."),

    (4, "Mapp v Ohio", "hard",
     "What is the exclusionary rule, and what are the arguments for and against it?",
     "The exclusionary rule bars illegally obtained evidence from trial; supporters argue it deters police misconduct, while critics argue it lets guilty defendants go free.",
     json.dumps(["The exclusionary rule requires all evidence to be presented at trial regardless of how it was obtained.",
                  "The exclusionary rule applies only to civil cases, not criminal trials.",
                  "There is no exclusionary rule in American law; all evidence is admissible if relevant."]),
     "The exclusionary rule, established in Weeks v United States (1914) and extended to states in Mapp v Ohio (1961), requires courts to exclude evidence obtained through unconstitutional searches and seizures. Supporters argue it deters police misconduct by removing the incentive for illegal searches. Critics argue it allows guilty defendants to go free on 'technicalities' and undermines public safety. The rule has several exceptions including the good faith exception, inevitable discovery doctrine, and independent source doctrine."),

    (4, "Mapp v Ohio", "medium",
     "How did Mapp v Ohio change the relationship between federal and state law enforcement?",
     "It required state and local police to follow the same Fourth Amendment standards as federal law enforcement, creating a uniform national standard.",
     json.dumps(["It gave state police greater authority than federal police in conducting searches.",
                  "It had no effect on state law enforcement because the Fourth Amendment already applied to them.",
                  "It eliminated the need for search warrants at all levels of government."]),
     "Before Mapp v Ohio, there was a significant gap between federal and state law enforcement regarding the Fourth Amendment. Federal agents had to follow Fourth Amendment restrictions because of the exclusionary rule in federal courts, but state and local police faced no such consequence for unconstitutional searches because state courts could still admit the evidence. Mapp closed this gap, establishing that the same constitutional standards apply to all law enforcement officers, whether federal, state, or local."),

    (4, "Mapp v Ohio", "easy",
     "What was the 'silver platter doctrine,' and how did Mapp v Ohio affect it?",
     "The silver platter doctrine allowed state evidence obtained illegally to be used in federal court; Mapp effectively ended it by applying the exclusionary rule to states.",
     json.dumps(["The silver platter doctrine required police to present evidence on a silver platter during trials.",
                  "The silver platter doctrine was a rule about proper courtroom etiquette.",
                  "The silver platter doctrine gave the President the power to override court decisions."]),
     "The silver platter doctrine was a legal principle that allowed state or local police to illegally obtain evidence and hand it over ('on a silver platter') to federal prosecutors for use in federal court, since the exclusionary rule only applied to federal officers. The doctrine was partially ended by Elkins v United States (1960) and completely eliminated by Mapp v Ohio (1961), which made the exclusionary rule applicable to all courts regardless of whether federal, state, or local officers obtained the evidence."),

    # Roe v Wade / Reproductive rights (4)
    (4, "Roe v Wade", "medium",
     "What did the Supreme Court rule in Roe v Wade (1973)?",
     "The Court recognized a constitutional right to privacy that protects a woman's decision to have an abortion, with limits based on trimesters of pregnancy.",
     json.dumps(["The Court ruled that abortion is illegal in all circumstances and at all stages of pregnancy.",
                  "The Court ruled that states have unlimited authority to regulate all medical procedures.",
                  "The Court ruled that the federal government must fund all abortion procedures."]),
     "In Roe v Wade (1973), the Supreme Court ruled 7-2 that a woman's right to choose an abortion fell within the right to privacy protected by the Due Process Clause of the Fourteenth Amendment. The Court established a trimester framework: in the first trimester, states could not regulate abortion; in the second, states could regulate to protect maternal health; in the third, states could prohibit abortion except to protect the mother's life or health. This framework was later modified by Planned Parenthood v Casey (1992) and ultimately overturned by Dobbs v Jackson Women's Health Organization (2022)."),

    (4, "Roe v Wade", "hard",
     "What amendment was the basis for the privacy right in Roe v Wade, and what constitutional principle did the Court draw on?",
     "The Fourteenth Amendment's Due Process Clause; the Court drew on the substantive due process doctrine, which protects fundamental rights not explicitly listed in the Constitution.",
     json.dumps(["The Second Amendment's right to bear arms, applied through the Commerce Clause.",
                  "The First Amendment's free speech clause, applied through the Tenth Amendment.",
                  "The Sixth Amendment's right to counsel, applied through the Eighth Amendment."]),
     "Roe v Wade relied on the Fourteenth Amendment's Due Process Clause and the doctrine of substantive due process — the principle that the Due Process Clause protects certain fundamental rights not explicitly enumerated in the Constitution. The Court traced this doctrine through a line of privacy cases including Griswold v Connecticut (1965), which found a right to marital privacy in the 'penumbras' of the Bill of Rights. Critics argued that the right to abortion was not deeply rooted in American history and tradition, which became the reasoning used in Dobbs v Jackson (2022) to overturn Roe."),

    (4, "Roe v Wade", "medium",
     "What was the impact of Dobbs v Jackson Women's Health Organization (2022) on constitutional law?",
     "It overturned Roe v Wade and Planned Parenthood v Casey, returning the authority to regulate abortion to individual states.",
     json.dumps(["It expanded abortion rights nationwide by establishing a constitutional right to abortion in all fifty states.",
                  "It had no effect because Roe v Wade had already been overturned by a previous case.",
                  "It made abortion a federal crime punishable by imprisonment."]),
     "Dobbs v Jackson Women's Health Organization (2022) overturned both Roe v Wade (1973) and Planned Parenthood v Casey (1992). The Court held that the Constitution does not confer a right to abortion, and that authority to regulate abortion is returned to the people and their elected representatives. This decision has resulted in a patchwork of state laws — some states have banned most abortions, others have protected the right to abortion, and still others have restrictions at various stages of pregnancy."),

    (4, "Roe v Wade", "easy",
     "What constitutional concept did Roe v Wade base its decision on?",
     "The right to privacy.",
     json.dumps(["The right to free speech.",
                  "The right to bear arms.",
                  "The right to a jury trial."]),
     "Roe v Wade was based on a constitutional right to privacy, which the Court found to be implied by several amendments in the Bill of Rights. The right to privacy had been previously recognized in Griswold v Connecticut (1965), which struck down a Connecticut law banning contraceptives for married couples. The Court reasoned that this right to privacy was 'broad enough to encompass a woman's decision whether or not to terminate her pregnancy.' The privacy doctrine has been used in cases involving contraception, marriage, family relationships, and other personal decisions."),

    # Executive orders and actions (5)
    (4, "Executive orders", "easy",
     "What is an executive order?",
     "A directive issued by the President that manages operations of the federal government and has the force of law.",
     json.dumps(["A law passed by Congress that the President must sign within 24 hours.",
                  "A constitutional amendment proposed by the President.",
                  "A treaty negotiated between the President and a foreign government."]),
     "An executive order is a written directive issued by the President to manage the operations of the federal government. Executive orders have the force of law and are based on the President's constitutional authority (Article II) or authority delegated by Congress. Presidents have used executive orders to establish policies, create or modify federal agencies, direct law enforcement priorities, and manage national emergencies. However, executive orders cannot create new laws or appropriate money — they must be grounded in constitutional or statutory authority."),

    (4, "Executive orders", "medium",
     "How can Congress limit or override a presidential executive order?",
     "Congress can pass a law to override an executive order (subject to presidential veto) or defund its implementation through the power of the purse.",
     json.dumps(["Congress has no power to limit executive orders; they are beyond congressional authority.",
                  "Congress can only override executive orders with a unanimous vote of both chambers.",
                  "Only the Supreme Court has the power to override executive orders; Congress cannot."]),
     "Congress has several tools to check executive orders. It can pass a law that contradicts or overrides the executive order (subject to presidential veto, meaning a two-thirds majority is needed to override a veto). Congress can also refuse to fund the implementation of an executive order using its power of the purse. Additionally, federal courts can strike down executive orders that exceed presidential authority or violate the Constitution. The balance of power between presidential executive orders and congressional oversight is a recurring tension in American governance."),

    (4, "Executive orders", "medium",
     "What is a famous example of an executive order that had major historical significance?",
     "Executive Order 9066 (1942), which authorized the internment of Japanese Americans during World War II.",
     json.dumps(["Executive Order 1, which established the Supreme Court in 1789.",
                  "Executive Order 9981, which abolished Congress and gave the President legislative power.",
                  "There are no historically significant executive orders; they are all minor administrative directives."]),
     "Executive Order 9066, signed by President Franklin Roosevelt on February 19, 1942, authorized the Secretary of War to designate military areas from which 'any or all persons may be excluded.' This led to the forced relocation and internment of approximately 120,000 Japanese Americans, two-thirds of whom were U.S.-born citizens. The order was upheld by the Supreme Court in Korematsu v United States (1944), a decision now widely regarded as one of the worst in Court history. In 1988, President Reagan signed the Civil Liberties Act, formally apologizing and providing reparations."),

    (4, "Executive orders", "hard",
     "What limits does the Constitution place on the President's ability to issue executive orders?",
     "Executive orders must be grounded in constitutional authority or congressional delegation, cannot create new law, cannot appropriate funds, and are subject to judicial review.",
     json.dumps(["The Constitution places no limits on executive orders; the President can issue them on any subject.",
                  "Executive orders expire after 90 days unless renewed by Congress.",
                  "The President can only issue executive orders during wartime."]),
     "The Constitution does not explicitly mention executive orders, but it limits presidential power generally. Executive orders must be grounded in either the President's Article II constitutional powers or authority delegated by Congress. Key limitations include: they cannot create new law (that is Congress's power), they cannot appropriate money (power of the purse belongs to Congress), they cannot violate constitutional rights, and they are subject to judicial review. Youngstown Sheet & Tube Co. v Sawyer (1952) established that presidential power is at its 'lowest ebb' when acting contrary to Congress's expressed or implied will."),

    (4, "Executive orders", "easy",
     "Can a future President revoke a previous President's executive orders?",
     "Yes, executive orders are not permanent law and can be revoked or modified by subsequent Presidents.",
     json.dumps(["No, executive orders become permanent law once signed and cannot be changed.",
                  "Only Congress can revoke executive orders, not future Presidents.",
                  "Executive orders can only be revoked by constitutional amendment."]),
     "Executive orders are not permanent — they remain in effect only as long as the current President chooses to keep them. A new President can revoke, modify, or replace any executive order issued by a predecessor. This is one of the reasons executive orders are controversial as policy tools: they can be easily undone by the next administration. Major policy shifts between administrations often involve revoking and replacing executive orders on topics ranging from immigration to environmental regulation to foreign policy."),

    # New Deal and Great Society (5)
    (4, "New Deal and Great Society", "easy",
     "What was the New Deal?",
     "A series of programs and reforms enacted by President Franklin Roosevelt in the 1930s to address the Great Depression, including relief, recovery, and reform measures.",
     json.dumps(["A treaty between the United States and European allies after World War II.",
                  "A constitutional amendment that abolished slavery and established civil rights.",
                  "A trade agreement between North American countries to eliminate tariffs."]),
     "The New Deal was President Franklin D. Roosevelt's comprehensive response to the Great Depression of the 1930s. It encompassed dozens of programs organized into three goals: relief for the unemployed and poor (like the Civilian Conservation Corps and Works Progress Administration), recovery of the economy (like the National Recovery Administration), and reform of the financial system (like the Glass-Steagall Act and Securities and Exchange Commission). The New Deal fundamentally expanded the federal government's role in American life."),

    (4, "New Deal and Great Society", "medium",
     "How did the New Deal change the relationship between the federal government and the economy?",
     "It established that the federal government has responsibility for managing the economy and providing a social safety net, significantly expanding federal power.",
     json.dumps(["It reduced the federal government's role in the economy by returning all regulatory power to the states.",
                  "It had no lasting effect on federal economic policy; the economy returned to its pre-Depression state after World War II.",
                  "It eliminated private enterprise and established a fully government-controlled economy."]),
     "Before the New Deal, the federal government played a limited role in economic management, with most regulation occurring at the state level. The New Deal established the principle that the federal government has both the responsibility and the authority to manage the economy, regulate private industry, and provide a social safety net. Key New Deal institutions — Social Security, the FDIC (bank deposit insurance), the SEC (securities regulation), minimum wage laws, and unemployment insurance — remain fundamental parts of American economic policy today."),

    (4, "New Deal and Great Society", "medium",
     "What was the Great Society, and who initiated it?",
     "President Lyndon B. Johnson's 1960s agenda of domestic programs aimed at eliminating poverty and racial injustice, including Medicare, Medicaid, and federal education funding.",
     json.dumps(["President Ronald Reagan's 1980s program of tax cuts and deregulation.",
                  "President Franklin Roosevelt's wartime program of industrial mobilization.",
                  "President Abraham Lincoln's post-Civil War plan for Southern reconstruction."]),
     "The Great Society was President Lyndon B. Johnson's ambitious domestic policy agenda, announced in 1964. It aimed to eliminate poverty and racial injustice through a sweeping set of federal programs. Major Great Society legislation included Medicare (health insurance for seniors), Medicaid (health insurance for the poor), the Elementary and Secondary Education Act (federal funding for schools), the Voting Rights Act of 1965, the Higher Education Act, Head Start, and the creation of the National Endowment for the Arts and Humanities. Together with the New Deal, the Great Society shaped the modern American welfare state."),

    (4, "New Deal and Great Society", "hard",
     "How did the Supreme Court's approach to federal power change from the early New Deal to its end?",
     "The Court initially struck down New Deal programs as exceeding federal power, then reversed course after FDR's court-packing threat, adopting a broad interpretation of the Commerce Clause.",
     json.dumps(["The Court consistently supported all New Deal programs from the beginning with no resistance.",
                  "The Court dissolved itself and was replaced by a new body appointed entirely by Roosevelt.",
                  "The Court never ruled on any New Deal legislation, leaving all constitutional questions unresolved."]),
     "The Supreme Court initially struck down key New Deal programs as exceeding Congress's power under the Commerce Clause. In Schechter Poultry Corp. v United States (1935), the Court invalidated the National Industrial Recovery Act. But after Roosevelt proposed his 'court-packing plan' (Judicial Procedures Reform Bill of 1937) to add more justices, the Court began upholding New Deal legislation. In West Coast Hotel Co. v Parrish (1937), the Court reversed its previous position on minimum wage laws. This 'switch in time that saved nine' fundamentally changed constitutional law by expanding Congress's Commerce Clause power."),

    (4, "New Deal and Great Society", "easy",
     "Which New Deal program created a system of retirement benefits for elderly Americans that still exists today?",
     "Social Security, established by the Social Security Act of 1935.",
     json.dumps(["Medicare, which was created during the Civil War.",
                  "The Federal Reserve, which was established in 1776.",
                  "The GI Bill, which provided housing loans to World War I veterans."]),
     "The Social Security Act of 1935, one of the most significant and enduring New Deal programs, created a federal system of old-age benefits (retirement insurance), unemployment insurance, and aid to dependent children. Funded through payroll taxes on workers and employers, Social Security has become the largest single program in the federal budget. While often associated with the New Deal, Medicare (health insurance for seniors) and Medicaid (health insurance for the poor) were actually created 30 years later as part of President Johnson's Great Society programs in 1965."),

    # 1st Amendment free speech deeper (5)
    (4, "First Amendment free speech", "medium",
     "What is the 'clear and present danger' test, and which case established it?",
     "A test for limiting free speech when words are used in such circumstances that they create a clear and present danger of bringing about substantive evils; established in Schenck v United States (1919).",
     json.dumps(["A test that allows the government to ban any speech that could potentially offend someone.",
                  "A test that prohibits all government restrictions on speech under any circumstances.",
                  "A test that applies only to commercial advertising, not political speech."]),
     "The 'clear and present danger' test was established by Justice Oliver Wendell Holmes in Schenck v United States (1919). Holmes wrote that 'the question in every case is whether the words used are used in such circumstances and are of such a nature as to create a clear and present danger that they will bring about the substantive evils that Congress has a right to prevent.' The test attempted to balance free speech with national security concerns during wartime, though it was used to uphold convictions in several controversial cases during the Red Scare era."),

    (4, "First Amendment free speech", "hard",
     "How did the 'imminent lawless action' test replace the 'clear and present danger' test?",
     "The Brandenburg test (1969) requires that speech be directed to inciting imminent lawless action AND likely to produce such action — a higher bar than the clear and present danger test.",
     json.dumps(["The imminent lawless action test was more restrictive of speech, making it easier to prosecute speakers.",
                  "The two tests are identical; no change occurred.",
                  "The imminent lawless action test applies only to written speech, not spoken words."]),
     "In Brandenburg v Ohio (1969), the Supreme Court replaced the clear and present danger test with a stricter standard for punishing advocacy of illegal conduct. The Brandenburg test requires that (1) the speech is directed to inciting or producing imminent lawless action, AND (2) the speech is likely to incite or produce such action. This significantly raised the bar for restricting speech — mere advocacy of illegal activity, no matter how strongly worded, is protected unless it meets both prongs. This remains the governing standard for incitement cases today."),

    (4, "First Amendment free speech", "medium",
     "What types of speech are NOT protected by the First Amendment?",
     "Incitement, true threats, obscenity, defamation, fraud, and speech integral to criminal conduct are among the categories not protected.",
     json.dumps(["All speech is absolutely protected; there are no exceptions under any circumstances.",
                  "Only speech that directly criticizes the government is unprotected.",
                  "Only written speech is protected; spoken words have no First Amendment protection."]),
     "While the First Amendment provides broad protection for speech, several categories are not protected. These include: incitement of imminent lawless action (Brandenburg test), true threats (direct threats of violence against individuals), obscenity (defined by the Miller test: community standards, patently offensive, lacking serious value), defamation (false statements that harm reputation), fraud and perjury, child pornography, speech integral to criminal conduct, and fighting words. The government can regulate these categories without violating the First Amendment."),

    (4, "First Amendment free speech", "easy",
     "What does the First Amendment's free speech clause protect?",
     "It protects the right to express ideas and opinions without government censorship or punishment, with certain limited exceptions.",
     json.dumps(["It protects only speech that the government approves of in advance.",
                  "It protects the right to say anything at any time without any consequences whatsoever.",
                  "It protects only written speech published in newspapers."]),
     "The First Amendment states that 'Congress shall make no law... abridging the freedom of speech.' This protects a broad range of expression including spoken words, written text, symbolic speech (like flag burning), and digital communication. However, free speech is not absolute — the government can impose reasonable time, place, and manner restrictions, and certain categories of speech (incitement, threats, obscenity, defamation) receive limited or no protection. The First Amendment applies to all levels of government through the Fourteenth Amendment."),

    (4, "First Amendment free speech", "hard",
     "What is symbolic speech, and how has the Supreme Court protected it?",
     "Symbolic speech is conduct that communicates a message (like flag burning, armbands, or protests); the Court has protected it under the First Amendment as long as it is not obscene or threatening.",
     json.dumps(["Symbolic speech is a legal term for government-issued propaganda.",
                  "Symbolic speech is not protected because only spoken words qualify as speech under the First Amendment.",
                  "Symbolic speech refers exclusively to sign language used by deaf Americans."]),
     "Symbolic speech (also called expressive conduct) is non-verbal conduct that communicates a message and is protected by the First Amendment. In Texas v Johnson (1989), the Court ruled that burning the American flag as political protest is protected symbolic speech. In Tinker v Des Moines (1969), the Court protected students wearing black armbands to protest the Vietnam War. The Court has held that the government cannot restrict symbolic speech simply because society finds it offensive. However, symbolic speech can be regulated if it involves illegal conduct beyond the expressive element (like blocking traffic during a protest)."),

    # Criminal procedure deeper (5)
    (4, "Criminal procedure rights", "medium",
     "What is the exclusionary rule's 'good faith exception'?",
     "Evidence obtained by officers acting in good faith on a warrant later found to be defective may still be admissible.",
     json.dumps(["The good faith exception allows police to search without any warrant if they believe they have probable cause.",
                  "The good faith exception means that evidence is always admissible if the officer had good intentions.",
                  "The good faith exception applies only to traffic stops, not home searches."]),
     "The good faith exception to the exclusionary rule, established in United States v Leon (1984), allows evidence obtained by police officers acting in reasonable, good-faith reliance on a warrant that is later found to be defective. The exception applies when the warrant is invalid due to a technical error (like a clerk's mistake) rather than deliberate police misconduct or a lack of probable cause. The Court reasoned that the exclusionary rule's purpose is to deter police misconduct, and suppressing evidence obtained in good faith does not serve that purpose."),

    (4, "Criminal procedure rights", "medium",
     "What rights does the Sixth Amendment guarantee to criminal defendants?",
     "The right to a speedy and public trial, an impartial jury, to be informed of charges, to confront witnesses, to compel witnesses, and to have the assistance of counsel.",
     json.dumps(["The right to remain silent, the right to an attorney, and the right to a phone call.",
                  "The right to a jury trial, the right to free food during trial, and the right to choose the judge.",
                  "The Sixth Amendment guarantees no rights; all criminal rights are in the Fifth Amendment."]),
     "The Sixth Amendment provides several protections for criminal defendants: (1) the right to a speedy trial, preventing indefinite pretrial detention; (2) the right to a public trial, preventing secret proceedings; (3) the right to an impartial jury drawn from the state and district where the crime occurred; (4) the right to be informed of the nature and cause of the accusation; (5) the right to confront opposing witnesses (cross-examination); (6) the right to compulsory process to obtain favorable witnesses; and (7) the right to effective assistance of counsel."),

    (4, "Criminal procedure rights", "hard",
     "What is the difference between a 'stop and frisk' and a full search under Fourth Amendment law?",
     "A stop and frisk (Terry stop) requires only reasonable suspicion and allows a limited pat-down for weapons; a full search requires probable cause and a warrant (with exceptions).",
     json.dumps(["There is no difference; both require a warrant signed by a judge.",
                  "A stop and frisk requires higher proof than a full search.",
                  "A full search requires less proof than a stop and frisk."]),
     "Under Terry v Ohio (1968), police may briefly detain a person (a 'Terry stop') based on reasonable suspicion that criminal activity is afoot, which is a lower standard than probable cause. During such a stop, police may frisk the outer clothing for weapons if they have reasonable suspicion the person is armed. This is a limited exception to the Fourth Amendment's warrant requirement. A full search, by contrast, generally requires probable cause and a warrant (or an established exception like consent, plain view, or search incident to arrest)."),

    (4, "Criminal procedure rights", "easy",
     "What does 'Miranda rights' refer to?",
     "The rights that police must inform suspects of before custodial interrogation, including the right to remain silent and the right to an attorney.",
     json.dumps(["The rights granted to victims of crimes to be compensated for their losses.",
                  "The rights of jurors to be dismissed from duty for personal reasons.",
                  "The rights of Congress members to free speech on the House and Senate floors."]),
     "Miranda rights come from Miranda v Arizona (1966), which held that the Fifth Amendment's privilege against self-incrimination requires police to inform suspects of certain rights before custodial interrogation. These include: the right to remain silent, that anything said can be used against them in court, the right to an attorney, and that an attorney will be appointed if they cannot afford one. If police fail to provide these warnings, statements made during interrogation are generally inadmissible in court."),

    (4, "Criminal procedure rights", "medium",
     "What is 'due process of law' as guaranteed by the Fifth and Fourteenth Amendments?",
     "The principle that the government must follow fair and established legal procedures before depriving a person of life, liberty, or property.",
     json.dumps(["Due process means that all citizens receive identical outcomes in court regardless of circumstances.",
                  "Due process applies only to civil cases, not criminal proceedings.",
                  "Due process is a procedural formality with no substantive meaning."]),
     "Due process of law appears in both the Fifth Amendment (applying to the federal government) and the Fourteenth Amendment (applying to states). It has two dimensions: procedural due process requires fair legal procedures (notice, hearing, impartial tribunal) before the government deprives a person of life, liberty, or property. Substantive due process protects fundamental rights from government interference even if proper procedures are followed. Due process is one of the most important concepts in constitutional law, serving as a foundation for protecting individual rights against arbitrary government action."),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
for q in questions:
    cur.execute(
        "INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation) VALUES (?,?,?,?,?,?,?)",
        q
    )
conn.commit()
print(f"Inserted {len(questions)} D4 questions")
conn.close()
