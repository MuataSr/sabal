#!/usr/bin/env python3
"""Add D3 questions batch 3: deeper founding documents, ratification, Constitutional Convention."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Constitutional Convention deeper (5)
    (3, "Constitutional Convention", "medium",
     "What was the Virginia Plan proposed at the Constitutional Convention?",
     "A plan for a strong national government with three branches, a bicameral legislature with representation based on state population, and the power to veto state laws.",
     json.dumps(["A plan for a weak central government that preserved state sovereignty and had a unicameral legislature.",
                  "A plan to maintain the Articles of Confederation with minor amendments.",
                  "A plan for a monarchy with a king as the chief executive and no legislative branch."]),
     "The Virginia Plan, proposed by Edmund Randolph and largely drafted by James Madison, called for a strong national government with three branches (legislative, executive, and judicial). Its most controversial feature was a bicameral legislature with both houses apportioned by state population — giving large states like Virginia more representation. It also gave Congress the power to veto state laws. Small states opposed the Virginia Plan because they feared being dominated by larger states, leading to the Great Compromise that created the current bicameral system."),

    (3, "Constitutional Convention", "medium",
     "What was the New Jersey Plan, and how did it differ from the Virginia Plan?",
     "The New Jersey Plan proposed a unicameral legislature with equal state representation and limited additional powers for the national government, preserving more state sovereignty.",
     json.dumps(["The New Jersey Plan proposed eliminating the national government entirely and returning to British rule.",
                  "The New Jersey Plan was identical to the Virginia Plan but with different terminology.",
                  "The New Jersey Plan proposed a unicameral legislature based on population with no executive branch."]),
     "The New Jersey Plan, proposed by William Paterson, was the small states' response to the Virginia Plan. It kept the unicameral structure of the Articles of Confederation but added the power to tax and regulate commerce. Each state would have equal representation regardless of population, protecting small states from being dominated. The plan also created a weak plural executive (multiple executives) rather than a single president. The conflict between the Virginia and New Jersey Plans was resolved by the Great Compromise, which combined elements of both."),

    (3, "Constitutional Convention", "hard",
     "What was the Three-Fifths Compromise, and what problem did it solve?",
     "The Three-Fifths Compromise counted each enslaved person as three-fifths of a person for taxation and representation purposes, balancing the interests of slave and free states.",
     json.dumps(["It required that three-fifths of all voters approve any federal law before it could take effect.",
                  "It gave the President the power to veto three-fifths of congressional legislation.",
                  "It limited the number of representatives any single state could send to Congress."]),
     "The Three-Fifths Compromise resolved a critical dispute between Northern and Southern states at the Constitutional Convention. Southern states wanted enslaved people counted fully for representation in the House (giving them more representatives) but not at all for taxation. Northern states wanted the opposite. The compromise counted each enslaved person as three-fifths of a person for both taxation and representation. This gave Southern states additional political power while acknowledging the Northern position on taxation. The compromise was superseded by the Fourteenth Amendment after the Civil War."),

    (3, "Constitutional Convention", "easy",
     "When and where was the Constitutional Convention held?",
     "In Philadelphia, Pennsylvania, during the summer of 1787.",
     json.dumps(["In New York City in 1776, immediately after the Declaration of Independence.",
                  ("In Boston, Massachusetts, in 1791, after the Bill of Rights was ratified."),
                  "In Washington, D.C., in 1800, after the federal government moved to the capital."]),
     "The Constitutional Convention (also called the Philadelphia Convention or the Federal Convention) met from May 25 to September 17, 1787, in Philadelphia's Independence Hall. Originally convened to revise the Articles of Confederation, the delegates quickly decided to draft an entirely new frame of government. Fifty-five delegates from twelve states attended (Rhode Island boycotted), with George Washington presiding. The convention was conducted in secrecy — the windows were kept shut despite the summer heat to prevent outside observers from learning of the debates."),

    (3, "Constitutional Convention", "hard",
     "Why was the Constitutional Convention conducted in secrecy, and what was the result?",
     "Delegates wanted frank debate without public pressure; the result was a Constitution that could be debated and ratified without prior political interference.",
     json.dumps(["The convention was secret because it was illegal and delegates feared arrest by British authorities.",
                  "The convention was not secret; all proceedings were published in daily newspapers.",
                  "The convention was secret because only three delegates actually attended and they wanted to hide this fact."]),
     "The Constitutional Convention adopted a strict rule of secrecy — delegates could not reveal the proceedings to anyone. James Madison's detailed notes, which were not published until after his death in 1836, are our primary record of the debates. The secrecy served several purposes: it allowed delegates to change their positions without public embarrassment, prevented outside interest groups from pressuring delegates, and ensured that the Constitution would be presented as a complete package for ratification rather than as individual provisions that could be picked apart. This approach was crucial to the Constitution's ultimate success."),

    # Ratification deeper (5)
    (3, "Constitutional ratification", "medium",
     "How many states were required to ratify the Constitution before it could take effect?",
     "Nine of the thirteen states, as specified in Article VII.",
     json.dumps(["All thirteen states had to unanimously ratify the Constitution.",
                  "A simple majority of seven states was sufficient.",
                  "Twelve states were required, with only one allowed to reject it."]),
     "Article VII of the Constitution specified that ratification by conventions in nine states would be sufficient to establish the Constitution among those states. The Framers chose state conventions rather than state legislatures for ratification, believing that conventions would better represent the will of the people. Delaware was the first to ratify (December 7, 1787), and New Hampshire became the ninth state on June 21, 1788, making the Constitution officially effective. The remaining four states eventually ratified, with Rhode Island being the last in 1790."),

    (3, "Constitutional ratification", "medium",
     "What was the Massachusetts Compromise during the ratification debate?",
     "Anti-Federalists agreed to ratify the Constitution in exchange for a promise that a Bill of Rights would be added as the first order of business.",
     json.dumps(["Massachusetts refused to ratify and seceded from the union permanently.",
                  "Massachusetts proposed that the Constitution be rewritten entirely in simpler language.",
                  "Massachusetts demanded that the capital be moved to Boston in exchange for ratification."]),
     "The Massachusetts Compromise was a critical turning point in the ratification debate. Massachusetts was closely divided between Federalists and Anti-Federalists. The compromise — proposed by John Hancock and Samuel Adams — was that Massachusetts would ratify the Constitution with a recommendation that amendments (a Bill of Rights) be added. This formula was adopted by several other states and was instrumental in securing ratification. It allowed the Constitution to be adopted while addressing Anti-Federalists' primary concern about individual liberties."),

    (3, "Constitutional ratification", "hard",
     "What were the Federalist Papers primarily written to address, and what was their impact on the ratification debate?",
     "They were written to persuade New York to ratify the Constitution; their long-term impact far exceeded their immediate goal as they became the definitive interpretation of constitutional principles.",
     json.dumps(["They were written to persuade Virginia to reject the Constitution and keep the Articles of Confederation.",
                  "They were written after the Constitution was ratified and had no impact on the ratification process.",
                  "They were written to explain British common law to American colonists unfamiliar with legal principles."]),
     "The Federalist Papers were published in New York newspapers from October 1787 to May 1788 to influence the New York ratification convention. Their immediate impact is debated — New York ratified by only a narrow margin (30-27), and it is unclear how many delegates were actually persuaded by the essays. However, their long-term significance is enormous. Federalist No. 10 (Madison's argument on factions), No. 51 (separation of powers), and No. 78 (judicial independence) remain among the most cited works in American constitutional law and Supreme Court decisions."),

    (3, "Constitutional ratification", "easy",
     "Which state was the first to ratify the Constitution?",
     "Delaware, on December 7, 1787.",
     json.dumps(["Virginia, on July 4, 1776.",
                  "Pennsylvania, on September 17, 1787.",
                  "New York, on March 4, 1789."]),
     "Delaware became the first state to ratify the Constitution on December 7, 1787, with a unanimous 30-0 vote in its state convention. For this reason, Delaware is known as 'The First State.' The ratification vote was unanimous because Delaware's delegates recognized that as a small state, the new Constitution offered better protection of its interests than the Articles of Confederation. The speed and unanimity of Delaware's ratification helped build momentum for ratification in other states."),

    (3, "Constitutional ratification", "medium",
     "Why did Rhode Island initially refuse to participate in the Constitutional Convention or ratify the Constitution?",
     "Rhode Island feared that a strong central government would threaten its economic independence and the interests of its merchant class, which benefited from the weak Articles of Confederation.",
     json.dumps(["Rhode Island was the smallest state and was not invited to the convention.",
                  "Rhode Island's delegates all died of illness before the convention began.",
                  "Rhode Island supported the Constitution unconditionally and was the first to ratify."]),
     "Rhode Island was the only state that refused to send delegates to the Constitutional Convention, largely because its merchant class benefited from the weak central government under the Articles of Confederation. Under the Articles, Rhode Island could print its own paper money and impose tariffs on other states, giving it economic advantages. Rhode Island was also the last state to ratify the Constitution (May 29, 1790), doing so only after the federal government threatened to treat it as a foreign nation and after the Bill of Rights had been proposed by Congress."),

    # Articles of Confederation deeper (5)
    (3, "Articles of Confederation", "medium",
     "What was the major weakness of the Articles of Confederation that led to its replacement?",
     "The national government had no power to tax, regulate commerce, or enforce laws, making it unable to address national problems.",
     json.dumps(["The Articles gave the national government too much power over the states.",
                  "The Articles established a monarchy that the states found unacceptable.",
                  "The Articles worked perfectly and were replaced only because they were too old."]),
     "The Articles of Confederation created a national government that was intentionally weak, reflecting the states' fear of centralized power after their experience with British rule. The major weaknesses included: no power to tax (the government could only request funds from states, which often refused), no power to regulate interstate or foreign commerce, no executive branch to enforce laws, no national judiciary, the requirement of unanimity for amendments, and no power to raise a standing army. Shays' Rebellion (1786-87) exposed these weaknesses and convinced many that a stronger national government was necessary."),

    (3, "Articles of Confederation", "hard",
     "What was Shays' Rebellion, and how did it influence the movement to replace the Articles of Confederation?",
     "An armed uprising of Massachusetts farmers protesting debt and taxes that the weak national government could not suppress, convincing many leaders that a stronger federal government was needed.",
     json.dumps(["A British military invasion that the Articles of Confederation successfully repelled, proving the system worked.",
                  "A peaceful protest in Virginia that was violently suppressed by the national government, causing public outrage.",
                  "A political debate in Congress that resulted in the immediate repeal of the Articles."]),
     "Shays' Rebellion (1786-87) was an armed uprising in western Massachusetts led by Daniel Shays, a Revolutionary War veteran. Farmers facing debt, high taxes, and property foreclosures attacked courthouses to prevent debt proceedings. Under the Articles of Confederation, the national government had no army to respond and could not force Massachusetts to accept federal assistance. The rebellion was eventually suppressed by a state-funded militia, but it alarmed national leaders including George Washington and James Madison, who saw it as evidence that the weak national government could not maintain order."),

    (3, "Articles of Confederation", "medium",
     "What was the Northwest Ordinance of 1787, and why is it significant?",
     "The Northwest Ordinance established a process for admitting new states from the Northwest Territory and banned slavery there; it showed that the Confederation Congress could achieve significant accomplishments.",
     json.dumps(["The Northwest Ordinance was a military alliance between the states and Native American tribes.",
                  "The Northwest Ordinance established the first national currency under the Articles of Confederation.",
                  "The Northwest Ordinance was a failed attempt to create a national university system."]),
     "The Northwest Ordinance of 1787 was arguably the most significant achievement of the Confederation Congress. It established a systematic process for creating new states from the Northwest Territory (Ohio, Indiana, Illinois, Michigan, Wisconsin, and part of Minnesota): a territory would be governed by Congress until its population reached 5,000 free adult males (at which point it could elect a legislature), and at 60,000 it could draft a state constitution and apply for statehood. The Ordinance also banned slavery in the territory and guaranteed basic rights including freedom of religion, trial by jury, and access to education."),

    (3, "Articles of Confederation", "easy",
     "How many branches of government did the Articles of Confederation create?",
     "One — a unicameral Congress. There was no executive or judicial branch at the national level.",
     json.dumps(["Three — legislative, executive, and judicial, just like the current Constitution.",
                  "Two — legislative and executive, but no judicial branch.",
                  "None — the Articles did not create any national government structure."]),
     "The Articles of Confederation created only one branch of national government: a unicameral (one-house) Congress where each state had one vote regardless of size or population. There was no separate executive branch (no president) and no national judiciary (no Supreme Court or federal courts). Congress had limited powers and no way to enforce its laws — it could request money and troops from states but could not compel compliance. This structural weakness was a primary reason the Articles were replaced by the Constitution, which established three separate branches."),

    (3, "Articles of Confederation", "hard",
     "How did the requirement for unanimous state consent under the Articles of Confederation affect governance?",
     "Amendments required unanimous approval from all thirteen states, making it virtually impossible to fix the Articles' weaknesses through reform.",
     json.dumps(["Unanimous consent was only required for declaring war; all other decisions needed a simple majority.",
                  "The Articles had no amendment process; the entire document had to be rewritten from scratch.",
                  "Unanimous consent was required but was easily achieved because all states agreed on every issue."]),
     "Under Article XIII of the Articles of Confederation, any alteration required the consent of Congress plus the ratification of every single state legislature. This unanimity requirement made meaningful reform essentially impossible. Even when delegates at the Constitutional Convention agreed that the Articles needed revision, the requirement that all thirteen states approve any change meant that formal amendment was not a viable path. This is why the Framers ultimately decided to draft an entirely new constitution, ratifying it through state conventions rather than state legislatures, with only nine states needed for it to take effect."),

    # Constitution deeper — Bill of Rights (5)
    (3, "Bill of Rights origins", "medium",
     "Why were the first ten amendments to the Constitution added?",
     "To address Anti-Federalist concerns that the Constitution lacked specific protections for individual liberties against federal power.",
     json.dumps(["The original Constitution explicitly prohibited any amendments, so the Bill of Rights was added illegally.",
                  "The Bill of Rights was part of the original Constitution drafted in 1787 and was not a later addition.",
                  "The British government required a Bill of Rights as a condition of American independence."]),
     "The Bill of Rights was added to address the primary Anti-Federalist objection to the Constitution: the lack of explicit protections for individual liberties. During ratification, several states (including Massachusetts, Virginia, and New York) ratified on the condition that amendments would be added. James Madison, initially skeptical that a bill of rights was necessary, became its principal author in the First Congress. He drew from existing state constitutions, the Virginia Declaration of Rights (written by George Mason), and the English Bill of Rights. The ten amendments were ratified by the states by December 15, 1791."),

    (3, "Bill of Rights origins", "medium",
     "How did the First Amendment protect religious freedom differently from previous state approaches?",
     "It prohibited the federal government from establishing a religion or interfering with free exercise, creating a separation between church and state at the national level.",
     json.dumps(["It established Christianity as the official religion of the United States.",
                  "It prohibited all religious practice in public spaces.",
                  "It required all citizens to attend church services regularly."]),
     "The First Amendment's Religion Clauses — 'Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof' — created a dual protection: the Establishment Clause prevents the federal government from creating an official religion or favoring one religion over another, while the Free Exercise Clause prevents the government from interfering with individuals' religious practices. This was revolutionary because several states still had established churches at the time. Thomas Jefferson later described it as building 'a wall of separation between Church and State.'"),

    (3, "Bill of Rights origins", "hard",
     "Why did James Madison initially oppose adding a Bill of Rights to the Constitution?",
     "Madison argued that enumerating some rights might imply the government could restrict unlisted rights, and that the Constitution's structure already limited government power sufficiently.",
     json.dumps(["Madison believed that individual rights were unimportant and should not be protected.",
                  "Madison wanted to add a Bill of Rights but was overruled by George Washington.",
                  "Madison opposed the Bill of Rights because it was written in French."]),
     "In Federalist No. 84, Alexander Hamilton (reflecting a position also held by Madison at the time) argued that a Bill of Rights was 'not only unnecessary in the proposed Constitution, but would even be dangerous.' The concern was that listing specific rights might imply that the government retained power over rights not listed. Madison's solution was the Ninth Amendment ('The enumeration in the Constitution, of certain rights, shall not be construed to deny or disparage others retained by the people'), which addressed this concern by acknowledging that people have additional rights beyond those listed."),

    (3, "Bill of Rights origins", "easy",
     "How many amendments are in the Bill of Rights?",
     "Ten amendments.",
     json.dumps(["Twelve amendments.",
                  "Five amendments.",
                  "Twenty-seven amendments."]),
     "The Bill of Rights consists of the first ten amendments to the Constitution, ratified on December 15, 1791. Congress originally approved twelve amendments in 1789, but only ten were ratified by the states at that time. The two unratified amendments dealt with the ratio of representatives to population (which would have resulted in over 6,000 representatives today) and congressional pay (which was eventually ratified as the Twenty-Seventh Amendment in 1992, over 200 years later). December 15 is now celebrated as Bill of Rights Day."),

    (3, "Bill of Rights origins", "medium",
     "What is the Ninth Amendment, and why is it important?",
     "The Ninth Amendment states that listing certain rights in the Constitution does not deny or disparage other rights retained by the people.",
     json.dumps(["The Ninth Amendment gives Congress unlimited power to create new rights through legislation.",
                  "The Ninth Amendment prohibits all forms of taxation.",
                  "The Ninth Amendment establishes the President's power to veto amendments."]),
     "The Ninth Amendment states: 'The enumeration in the Constitution, of certain rights, shall not be construed to deny or disparage others retained by the people.' It was Madison's solution to the concern that listing specific rights might imply the government could restrict any rights not mentioned. The amendment recognizes that the people have fundamental rights beyond those explicitly listed in the Bill of Rights. While the Ninth Amendment has been cited in cases involving privacy rights and personal autonomy, its precise meaning and application remain debated among scholars and judges."),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
for q in questions:
    cur.execute(
        "INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation) VALUES (?,?,?,?,?,?,?)",
        q
    )
conn.commit()
print(f"Inserted {len(questions)} D3 questions")
conn.close()
