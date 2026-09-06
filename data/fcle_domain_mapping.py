#!/usr/bin/env python3
"""
FCLE Domain Mapping — maps OpenStax American Government 2e KB sections
to the 4 Florida Civic Literacy Exam domains.

FCLE Domains:
  1. American Democracy — founding principles, citizen roles, political participation
  2. US Constitution — structure, branches, federalism, amendments
  3. Founding Documents — Declaration, Federalist Papers, Articles, Constitution
  4. Landmark Impact — Supreme Court cases, landmark legislation, executive actions
"""

# content_id → fcle_domain (1-4)
DOMAIN_MAP = {
    # Chapter 1: American Government and Civic Engagement
    1: 1,   # 1.1 What is Government? → D1 (principles)
    2: 1,   # 1.2 Who Governs? → D1 (democracy theories)
    3: 1,   # 1.3 Engagement in a Democracy → D1 (citizen participation)

    # Chapter 2: The Constitution and Its Origins
    4: 3,   # 2.1 Pre-Revolutionary Period → D3 (historical context)
    5: 3,   # 2.2 Articles of Confederation → D3 (founding document)
    6: 3,   # 2.3 Development of the Constitution → D3 (Constitution as document)
    7: 3,   # 2.4 Ratification of the Constitution → D3 (Federalist Papers context)

    # Chapter 2 remainder
    8: 2,   # 2.5 Constitutional Change → D2 (amendment process)

    # Chapter 3: American Federalism
    9: 2,   # 3.1 Division of Powers → D2 (federalism)
    10: 2,  # 3.2 Evolution of American Federalism → D2
    11: 2,  # 3.3 Intergovernmental Relationships → D2
    12: 2,  # 3.4 Competitive Federalism Today → D2
    13: 2,  # 3.5 Advantages and Disadvantages → D2

    # Chapter 4: Civil Liberties
    14: 2,  # 4.1 What Are Civil Liberties? → D2 (Bill of Rights structure)
    15: 4,  # 4.2 Securing Basic Freedoms → D4 (1st Amendment cases)
    16: 4,  # 4.3 Rights of Suspects → D4 (4th-6th Amendment cases)
    17: 4,  # 4.4 Interpreting Bill of Rights → D4 (incorporation doctrine)

    # Chapter 5: Civil Rights
    18: 4,  # 5.1 What Are Civil Rights? → D4 (14th Amendment)
    19: 4,  # 5.2 African American Struggle → D4 (landmark cases + legislation)
    20: 4,  # 5.3 Fight for Women's Rights → D4 (19th Amendment, legislation)
    21: 4,  # 5.4 Civil Rights for Indigenous Groups → D4
    22: 4,  # 5.5 Equal Protection for Other Groups → D4

    # Chapter 6: Politics of Public Opinion
    23: 1,  # 6.1 Nature of Public Opinion → D1 (democratic participation)
    24: 1,  # 6.2 Measuring Public Opinion → D1
    25: 1,  # 6.3 What Does the Public Think? → D1
    26: 1,  # 6.4 Effects of Public Opinion → D1

    # Chapter 7: Voting and Elections
    27: 1,  # 7.1 Voter Registration → D1 (political participation)
    28: 1,  # 7.2 Voter Turnout → D1
    29: 1,  # 7.3 Elections → D1
    30: 1,  # 7.4 Campaigns and Voting → D1
    31: 1,  # 7.5 Direct Democracy → D1

    # Chapter 8: The Media
    32: 1,  # 8.1 What Is the Media? → D1 (media in democracy)
    33: 1,  # 8.2 Evolution of the Media → D1
    34: 1,  # 8.3 Regulating the Media → D1
    35: 1,  # 8.4 Impact of the Media → D1

    # Chapter 9: Political Parties
    36: 1,  # 9.1 What Are Parties? → D1 (political participation)
    37: 1,  # 9.2 Two-Party System → D1
    38: 1,  # 9.3 Shape of Modern Parties → D1
    39: 1,  # 9.4 Divided Government / Polarization → D1

    # Chapter 10: Interest Groups
    40: 1,  # 10.1 Interest Groups Defined → D1 (participation)
    41: 1,  # 10.2 Collective Action → D1
    42: 1,  # 10.3 Interest Groups as Participation → D1
    43: 1,  # 10.4 Pathways of Influence → D1
    44: 1,  # 10.5 Free Speech and Regulation → D1

    # Chapter 11: Congress
    45: 2,  # 11.1 Institutional Design → D2 (legislative branch)
    46: 2,  # 11.2 Congressional Elections → D2
    47: 2,  # 11.3 Congressional Representation → D2
    48: 2,  # 11.4 House and Senate Organizations → D2
    49: 2,  # 11.5 Legislative Process → D2

    # Chapter 12: The Presidency
    50: 2,  # 12.1 Design and Evolution → D2 (executive branch)
    51: 2,  # 12.2 Presidential Election Process → D2
    52: 2,  # 12.3 Organizing to Govern → D2
    53: 2,  # 12.4 The Public Presidency → D2
    54: 4,  # 12.5 Presidential Governance → D4 (executive actions)

    # Chapter 13: The Courts
    55: 2,  # 13.1 Guardians of Constitution → D2 (judicial branch)
    56: 2,  # 13.2 Dual Court System → D2
    57: 2,  # 13.3 Federal Court System → D2
    58: 2,  # 13.4 The Supreme Court → D2
    59: 4,  # 13.5 Judicial Decision-Making → D4 (how SCOTUS shapes law)

    # Chapter 14: State and Local Government
    60: 2,  # 14.1 State Power and Delegation → D2 (federalism)
    61: 2,  # 14.2 State Political Culture → D2
    62: 2,  # 14.3 Governors and State Legislatures → D2
    63: 2,  # 14.4 State Legislative Term Limits → D2
    64: 2,  # 14.5 County and City Government → D2

    # Chapter 15: The Bureaucracy
    65: 2,  # 15.1 Bureaucracy and Evolution → D2 (executive branch)
    66: 2,  # 15.2 Merit-Based Civil Service → D2
    67: 2,  # 15.3 Understanding Bureaucracies → D2
    68: 2,  # 15.4 Controlling the Bureaucracy → D2

    # Chapter 16: Domestic Policy
    69: 4,  # 16.1 What Is Public Policy? → D4 (policy context)
    70: 4,  # 16.2 Categorizing Public Policy → D4
    71: 4,  # 16.3 Policy Arenas → D4 (landmark legislation)
    72: 4,  # 16.4 Policymakers → D4
    73: 4,  # 16.5 Budgeting and Tax Policy → D4

    # Chapter 17: Foreign Policy
    74: 4,  # 17.1 Defining Foreign Policy → D4 (executive actions)
    75: 4,  # 17.2 Foreign Policy Instruments → D4
    76: 4,  # 17.3 Institutional Relations → D4
    77: 4,  # 17.4 Approaches to Foreign Policy → D4
}

# Domain metadata
DOMAINS = {
    1: {
        "name": "American Democracy",
        "description": "Founding principles of American democracy, including natural rights, social contract, limited government, popular sovereignty, and the role of citizens in political participation.",
        "topics": [
            "Natural rights philosophy (Locke, Montesquieu)",
            "Social contract theory",
            "Limited government and rule of law",
            "Popular sovereignty",
            "Citizen participation (voting, elections)",
            "Political parties and interest groups",
            "Public opinion and media",
            "Direct democracy (initiatives, referendums, recalls)",
        ],
        "fce_question_count": 20,
    },
    2: {
        "name": "US Constitution",
        "description": "Structure, function, and design of the US Constitution, including the three branches of government, federalism, separation of powers, checks and balances, and the amendment process.",
        "topics": [
            "Articles I-VII structure",
            "Legislative branch (Congress)",
            "Executive branch (Presidency)",
            "Judicial branch (Courts)",
            "Federalism and division of powers",
            "Separation of powers and checks and balances",
            "Amendment process",
            "Bill of Rights (structure and content)",
            "State and local government",
            "Bureaucracy",
        ],
        "fce_question_count": 20,
    },
    3: {
        "name": "Founding Documents",
        "description": "Key founding documents and their influence on American self-government, including the Declaration of Independence, Federalist Papers, Articles of Confederation, and the US Constitution.",
        "topics": [
            "Declaration of Independence",
            "Articles of Confederation",
            "US Constitution",
            "Federalist Papers (especially No. 10 and No. 51)",
            "Anti-Federalist arguments",
            "Constitutional Convention debates",
            "Ratification process",
        ],
        "fce_question_count": 20,
    },
    4: {
        "name": "Landmark Impact",
        "description": "Impact of landmark Supreme Court cases, landmark legislation, and executive actions on American law and society.",
        "topics": [
            "Supreme Court cases (Marbury v Madison, Brown v Board, Roe v Wade, etc.)",
            "Civil rights legislation (Civil Rights Act, Voting Rights Act)",
            "14th Amendment incorporation doctrine",
            "1st Amendment cases (free speech, religion, press)",
            "Criminal procedure cases (Miranda, Gideon, Mapp)",
            "Executive orders and actions",
            "New Deal and Great Society programs",
        ],
        "fce_question_count": 20,
    },
}


def get_distribution():
    """Return section count per domain for verification."""
    dist = {1: 0, 2: 0, 3: 0, 4: 0}
    for sid, domain in DOMAIN_MAP.items():
        dist[domain] += 1
    return dist


if __name__ == "__main__":
    dist = get_distribution()
    print("=== FCLE Domain Distribution ===")
    for d in sorted(dist):
        print(f"  D{d} {DOMAINS[d]['name']}: {dist[d]} sections")
    print(f"  Total: {sum(dist.values())} sections")
