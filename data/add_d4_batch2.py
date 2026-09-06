#!/usr/bin/env python3
"""Add D4 questions: Plessy, Dred Scott, Citizens United, Incorporation doctrine."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Plessy v Ferguson (5)
    (4, "Plessy v Ferguson", "easy",
     "In Plessy v Ferguson (1896), what was the Supreme Court's ruling regarding racial segregation?",
     "The Court upheld racial segregation under the 'separate but equal' doctrine.",
     json.dumps(["The Court ruled that all racial segregation was unconstitutional.",
                  "The Court ordered the immediate desegregation of all public facilities.",
                  "The Court ruled that segregation was permissible only in private businesses, not public ones."]),
     "The Supreme Court in Plessy v Ferguson (1896) established the 'separate but equal' doctrine, ruling that racial segregation did not violate the Fourteenth Amendment as long as facilities were supposedly equal. This decision effectively legalized segregation across the American South for nearly 60 years. The Court rejected Homer Plessy's argument that segregation violated his constitutional rights under the Equal Protection Clause."),

    (4, "Plessy v Ferguson", "medium",
     "What was the legal reasoning the Supreme Court used in Plessy v Ferguson to justify the 'separate but equal' doctrine?",
     "The Court argued that segregation did not imply inferiority and that the Fourteenth Amendment addressed political equality, not social equality.",
     json.dumps(["The Court cited the Commerce Clause to justify state segregation laws.",
                  "The Court ruled that the Fourteenth Amendment did not apply to state laws at all.",
                  "The Court found that Plessy had violated a valid federal law and had no standing to challenge state law."]),
     "Justice Henry Billings Brown, writing for the majority in Plessy, claimed that if segregation 'stamps the colored race with a badge of inferiority,' it was 'not by reason of anything found in the act, but solely because the colored race chooses to put that construction upon it.' The Court reasoned the Fourteenth Amendment was intended to establish political equality, not social equality, and thus did not prevent states from enacting segregation laws."),

    (4, "Plessy v Ferguson", "hard",
     "Which justice wrote the lone dissent in Plessy v Ferguson, and what was the core argument of that dissent?",
     "Justice John Marshall Harlan argued that the Constitution is color-blind and that segregation violated the principle of equal citizenship.",
     json.dumps(["Justice Oliver Wendell Holmes argued that segregation was a matter of states' rights under the Tenth Amendment.",
                  "Justice Louis Brandeis argued that segregation caused measurable psychological harm to Black Americans.",
                  "Justice Joseph McKenna argued that the case should be dismissed because Plessy was only one-eighth Black."]),
     "Justice John Marshall Harlan's dissent in Plessy became one of the most celebrated in Supreme Court history. He wrote: 'Our Constitution is color-blind, and neither knows nor tolerates classes among citizens.' Harlan argued that the Thirteenth and Fourteenth Amendments were specifically designed to eliminate racial distinctions in civil rights, and that the majority's 'separate but equal' reasoning betrayed the purpose of these amendments."),

    (4, "Plessy v Ferguson", "medium",
     "How did the Plessy v Ferguson decision affect American society and law for the next several decades?",
     "It provided legal justification for Jim Crow laws and racial segregation across the Southern United States.",
     json.dumps(["It led to the immediate passage of federal civil rights legislation.",
                  "It had little practical impact because Northern states already prohibited segregation.",
                  "It was quickly overturned by the Court within five years of the decision."]),
     "Plessy v Ferguson served as the legal foundation for the Jim Crow system of racial segregation in the American South from 1896 until 1954. Southern states passed laws mandating segregation in schools, transportation, restaurants, parks, and virtually every aspect of public life. The 'separate but equal' doctrine gave constitutional cover to state laws that enforced racial hierarchy and second-class citizenship for Black Americans."),

    (4, "Plessy v Ferguson", "easy",
     "What amendment did Homer Plessy argue was violated by Louisiana's Separate Car Act in Plessy v Ferguson?",
     "The Fourteenth Amendment's Equal Protection Clause.",
     json.dumps(["The First Amendment's Free Exercise Clause",
                  "The Fifth Amendment's Due Process Clause",
                  "The Thirteenth Amendment's prohibition on slavery"]),
     "Homer Plessy, who was one-eighth Black, deliberately violated Louisiana's Separate Car Act of 1890 by sitting in a whites-only railroad car. He argued that the law violated the Fourteenth Amendment's Equal Protection Clause, which guarantees that no state shall 'deny to any person within its jurisdiction the equal protection of the laws.' The Supreme Court rejected this argument, ruling 7-1 that separate accommodations did not violate equal protection."),

    # Dred Scott v Sandford (5)
    (4, "Dred Scott v Sandford", "easy",
     "What was the Supreme Court's decision in Dred Scott v Sandford (1857)?",
     "The Court ruled that African Americans, whether enslaved or free, could not be American citizens and therefore had no standing to sue in federal court.",
     json.dumps(["The Court ruled that slavery was unconstitutional and ordered Dred Scott's immediate freedom.",
                  "The Court ruled that Dred Scott was free because he had lived in free territories.",
                  "The Court refused to hear the case, citing lack of jurisdiction."]),
     "In Dred Scott v Sandford (1857), Chief Justice Roger Taney wrote for a 7-2 majority that African Americans were 'beings of an inferior order' who had 'no rights which the white man was bound to respect.' The Court declared that Scott, as a Black person, could not be a citizen and thus had no right to sue in federal court. The decision also struck down the Missouri Compromise as unconstitutional."),

    (4, "Dred Scott v Sandford", "medium",
     "Why did the Dred Scott decision declare the Missouri Compromise unconstitutional?",
     "The Court ruled that Congress had no power to prohibit slavery in the territories because doing so would violate slaveholders' Fifth Amendment property rights.",
     json.dumps(["The Court found the Missouri Compromise violated the First Amendment by restricting free speech about slavery.",
                  "The Court ruled the Missouri Compromise violated the Commerce Clause by restricting interstate movement of enslaved persons.",
                  "The Court declared that only states, not Congress, had authority over territorial governance."]),
     "The Dred Scott Court held that the Missouri Compromise of 1820, which prohibited slavery in certain territories, was unconstitutional because it deprived slaveholders of their property without due process of law, violating the Fifth Amendment. Chief Justice Taney argued that the Constitution protected the right to own property (including enslaved people) in all territories, meaning Congress could not ban slavery anywhere in the territories."),

    (4, "Dred Scott v Sandford", "hard",
     "How did the Dred Scott decision contribute to the political crisis that led to the Civil War?",
     "It intensified sectional conflict by ruling that Congress could not ban slavery in territories, making the slavery expansion debate constitutional rather than political.",
     json.dumps(["It was largely ignored because the North refused to enforce it, having no practical impact.",
                  "It led to an immediate compromise that temporarily resolved the slavery question.",
                  "It caused Southern states to secede immediately after the decision."]),
     "The Dred Scott decision was a catastrophe for national unity. By declaring that Congress had no power to restrict slavery in territories, it invalidated the central platform of the new Republican Party (keeping slavery out of territories). The decision outraged Northerners, energized the abolitionist movement, and made political compromise on slavery nearly impossible. Abraham Lincoln's 1858 debates with Stephen Douglas and his 1860 election were directly shaped by the controversy surrounding Dred Scott."),

    (4, "Dred Scott v Sandford", "medium",
     "Which constitutional provision did the Dred Scott majority interpret as protecting slaveholders' property rights in the territories?",
     "The Fifth Amendment's Due Process Clause.",
     json.dumps(["The Fourth Amendment's protection against unreasonable searches",
                  "The Tenth Amendment's reservation of powers to the states",
                  "The Article IV Privileges and Immunities Clause"]),
     "The Dred Scott Court held that the Fifth Amendment's Due Process Clause — specifically the Takings Clause ('nor shall private property be taken for public use, without just compensation') — prohibited Congress from banning slavery in the territories. The Court reasoned that enslaved people were property, and banning slavery in territories amounted to taking property without compensation. This interpretation was widely criticized and was effectively overturned by the Thirteenth Amendment."),

    (4, "Dred Scott v Sandford", "easy",
     "Who was Dred Scott and why did he file a lawsuit?",
     "Dred Scott was an enslaved man who sued for his freedom after living in free territories with his owner.",
     json.dumps(["Dred Scott was a free Black minister who sued for voting rights.",
                  "Dred Scott was a white abolitionist who sued on behalf of enslaved persons.",
                  "Dred Scott was a plantation owner who sued to prevent the emancipation of his workers."]),
     "Dred Scott was an enslaved man who had been taken by his owner, Dr. John Emerson, from Missouri (a slave state) to Illinois and the Wisconsin Territory (both free soil). After Emerson's death, Scott sued for his freedom in Missouri courts, arguing that his residence in free territory had made him free. After losing in Missouri courts, he pursued his case in federal court, ultimately reaching the Supreme Court."),

    # Citizens United v FEC (5)
    (4, "Citizens United v FEC", "easy",
     "What did the Supreme Court rule in Citizens United v FEC (2010)?",
     "The Court ruled that corporate spending on independent political communications is protected speech under the First Amendment.",
     json.dumps(["The Court ruled that corporations cannot make any political contributions whatsoever.",
                  "The Court upheld limits on corporate spending in federal elections.",
                  "The Court ruled that political action committees are unconstitutional."]),
     "In Citizens United v FEC (2010), the Supreme Court held 5-4 that the First Amendment prohibits the government from restricting independent political expenditures by corporations, unions, and other associations. The decision overturned parts of the Bipartisan Campaign Reform Act (McCain-Feingold) and the precedent of Austin v Michigan Chamber of Commerce, significantly expanding the role of money in American elections."),

    (4, "Citizens United v FEC", "medium",
     "What was the specific case that triggered the Citizens United litigation?",
     "Citizens United, a nonprofit, wanted to air a film critical of Hillary Clinton during the 2008 presidential primary.",
     json.dumps(["A labor union wanted to run television ads supporting a presidential candidate.",
                  "A corporation attempted to donate directly to a senator's re-election campaign.",
                  "A political party challenged the FEC's debate rules."]),
     "Citizens United, a conservative nonprofit, produced 'Hillary: The Movie,' a documentary critical of then-Senator Hillary Clinton during her 2008 presidential campaign. The FEC blocked the organization from advertising the film within 30 days of a primary election under the Bipartisan Campaign Reform Act. Citizens United challenged the restriction, and the Supreme Court used the case to broadly reconsider limits on independent political spending."),

    (4, "Citizens United v FEC", "hard",
     "What constitutional principle did the Citizens United majority rely on to reach its decision?",
     "The First Amendment protects political speech regardless of whether the speaker is a corporation or an individual.",
     json.dumps(["The Fifth Amendment Due Process Clause gives corporations the same rights as natural persons.",
                  "The Fourteenth Amendment Equal Protection Clause prevents discrimination against corporate speakers.",
                  "The Commerce Clause prevents federal regulation of corporate political activity."]),
     "Justice Kennedy's majority opinion in Citizens United rested on the principle that the First Amendment does not distinguish between speakers based on their corporate or individual identity. The Court rejected the argument that the government could restrict political speech based on the identity of the speaker. Kennedy wrote that 'If the First Amendment has any force, it prohibits Congress from fining or jailing citizens, or associations of citizens, for simply engaging in political speech.'"),

    (4, "Citizens United v FEC", "medium",
     "What prior legal precedent did Citizens United overturn regarding corporate political spending?",
     "It overturned Austin v Michigan Chamber of Commerce (1990), which had allowed restrictions on corporate independent expenditures.",
     json.dumps(["It overturned Buckley v Valeo, which had established contribution limits for individuals.",
                  "It overturned Wisconsin v Yoder, which had protected religious freedom.",
                  "It overturned Shaw v Reno, which had addressed racial gerrymandering."]),
     "Citizens United explicitly overruled Austin v Michigan Chamber of Commerce (1990), which had upheld Michigan's restriction on corporate independent expenditures. The Court also overruled part of McConnell v FEC (2003), which had upheld the McCain-Feingold law's restrictions on electioneering communications. These precedents had allowed the government to limit corporate spending on political speech, which Citizens United held violated the First Amendment."),

    (4, "Citizens United v FEC", "easy",
     "How did Citizens United affect campaign finance law in the United States?",
     "It removed restrictions on independent political spending by corporations and unions, leading to a significant increase in political spending.",
     json.dumps(["It eliminated all campaign finance regulations, allowing unlimited direct donations to candidates.",
                  "It had minimal impact because most corporate spending was already legal through PACs.",
                  "It strengthened the Bipartisan Campaign Reform Act by clarifying its scope."]),
     "Citizens United removed restrictions on independent expenditures by corporations, unions, and other organizations, leading to the rise of 'super PACs' that can spend unlimited amounts on political advertising as long as they do not coordinate directly with candidates. Political spending in federal elections increased dramatically after the decision, making it one of the most consequential campaign finance rulings in American history."),

    # 14th Amendment incorporation (5)
    (4, "Fourteenth Amendment incorporation", "easy",
     "What is the incorporation doctrine?",
     "The process by which the Supreme Court has applied Bill of Rights protections to the states through the Fourteenth Amendment.",
     json.dumps(["The process of adding new amendments to the Constitution through congressional action.",
                  "The process by which the federal government takes over state functions during emergencies.",
                  "The process of merging separate court cases into a single Supreme Court review."]),
     "The incorporation doctrine is the legal principle that the Fourteenth Amendment's Due Process Clause ('nor shall any State deprive any person of life, liberty, or property, without due process of law') makes most Bill of Rights protections applicable to the states. Before incorporation, the Bill of Rights limited only the federal government. Through incorporation, the Supreme Court has extended most Bill of Rights protections to state and local governments."),

    (4, "Fourteenth Amendment incorporation", "medium",
     "Which landmark case began the incorporation process?",
     "Gitlow v New York (1925), which incorporated the First Amendment's free speech protections against the states.",
     json.dumps(["Marbury v Madison (1803), which established judicial review.",
                  "Barron v Baltimore (1833), which held that the Bill of Rights did not apply to the states.",
                  "Brown v Board of Education (1954), which incorporated the Equal Protection Clause."]),
     "The incorporation process began with Gitlow v New York (1925), where the Supreme Court held that the First Amendment's free speech and free press protections applied to the states through the Fourteenth Amendment. Although Gitlow was convicted under New York's criminal anarchy law (the Court upheld his conviction), the case established the principle that fundamental Bill of Rights protections could be enforced against state governments."),

    (4, "Fourteenth Amendment incorporation", "hard",
     "What is the difference between 'selective incorporation' and 'total incorporation,' and which approach did the Supreme Court adopt?",
     "Selective incorporation applies protections one at a time; total incorporation would apply all at once. The Court adopted selective incorporation.",
     json.dumps(["Total incorporation applies all protections at once; selective applies them one at a time. The Court adopted total incorporation.",
                  "Selective incorporation only applies criminal procedure protections; total applies all civil liberties. The Court adopted selective.",
                  "Both approaches were rejected; the Court uses a balancing test instead."]),
     "The debate between selective and total incorporation was resolved in favor of selective incorporation, championed by Justice Benjamin Cardozo in Palko v Connecticut (1937). Cardozo argued that only those Bill of Rights protections 'implicit in the concept of ordered liberty' should be incorporated. Over time, the Court has incorporated nearly all provisions except the Third Amendment, the Fifth Amendment's grand jury requirement, and the Seventh Amendment's civil jury trial right."),

    (4, "Fourteenth Amendment incorporation", "medium",
     "Which of the following Bill of Rights protections has NOT been incorporated against the states?",
     "The requirement of a grand jury indictment for felony charges (Fifth Amendment).",
     json.dumps(["The protection against unreasonable searches and seizures (Fourth Amendment).",
                  "The right to counsel in criminal cases (Sixth Amendment).",
                  "The prohibition on cruel and unusual punishment (Eighth Amendment)."]),

     "Through selective incorporation, the Supreme Court has applied nearly all Bill of Rights protections to the states. The notable exceptions are the Third Amendment's prohibition on quartering soldiers (never incorporated because no case has required it), the Fifth Amendment's grand jury indictment requirement (not incorporated and never revisited), and the Seventh Amendment's right to a jury trial in civil cases (not incorporated)."),

    (4, "Fourteenth Amendment incorporation", "easy",
     "What clause of the Fourteenth Amendment is primarily used to incorporate Bill of Rights protections against the states?",
     "The Due Process Clause.",
     json.dumps(["The Equal Protection Clause",
                  "The Privileges or Immunities Clause",
                  "The Citizenship Clause"]),
     "Although the Fourteenth Amendment has several clauses, the Supreme Court has primarily used the Due Process Clause ('nor shall any State deprive any person of life, liberty, or property, without due process of law') to incorporate Bill of Rights protections. The Privileges or Immunities Clause was effectively rendered dormant by the Slaughter-House Cases (1873), and the Equal Protection Clause is used for discrimination cases rather than incorporation."),
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
