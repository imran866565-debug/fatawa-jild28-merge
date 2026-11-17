#!/usr/bin/env python3
"""Merge Jild 28 tashreeh chunks into jild-28.json.

Re-runnable: reads every jild-28-chunk-*.json listed in the manifest,
merges in chunk order, validates (unique ids, page coverage, zero
empty jawab), writes jild-28.json, and updates the manifest statuses.

INPUT (verified on disk by the parent):
  14 chunk files (no splits), 94 chunk items, volume_id 32. Source
  export ~/workspace/fatawa-app/content/jild-28.json: 637 rows but
  only 636 UNIQUE pages (p. 554 has TWO rows, both lesson 77, both
  covered in chunk 12's muqaddima-3 item, listed once). This is the
  Jild 16 precedent (543 rows, 542 unique pages), the Jild 26
  precedent (562 rows, 561 unique pages) and the Jild 27 precedent
  (645 rows, 642 unique pages). Validate the merged page union
  against the source export's 636 UNIQUE pages, NOT the 637 row
  count. Gaps (46, nothing invented): pp. 11-50 (40), 335, 355,
  364, 490, 492, 594 — every gap listed in the manifest's
  source_gaps and in each chunk's missing_pages (Jild 17 lesson).
  Inter-chunk gap inside NO chunk's span: p. 490 (chunk 10 ends
  489, chunk 11 starts 491). Validate against the chunk items'
  page union (636 pages), NOT range arithmetic.

COMBINE RULES (5 cases; parts ordered by min page; pages = UNION of
all parts' pages; notes = all parts' notes; start_page = min page;
all parts have empty sawal, so every combined sawal is 0):
  shamama-4-nufha-3:  2 parts -> 1, RENAME-THEN-COMBINE. Lesson
               535, nafha 3 (ind lil-hudur). Chunk 04
               shamama-4-nufha-3 [206-212] (jawab 5,650) + chunk 05
               nafha-3 [213-215] (jawab 2,200) -> ONE item
               'jild28-shamama-4-nufha-3', pages [206-215] (10 pp.),
               jawab 7,850. Evidence: p. 212 ends mid-example (9)
               of the ind list and p. 213 continues it. NOTE: chunk
               03's 'jild28-nafha-3' [120-122] is a DIFFERENT
               section (lesson 533) and KEEPS the plain id — the
               combine selector must pick ONLY the chunk-05 part
               (start_page 213). Net -1.
  shamama-4-nufha-14: 2 parts -> 1, RENAME-THEN-COMBINE. Lesson
               535, nafha 14 (Muhyiddin ka laqab). Chunk 05
               nafha-14 [254-258] (jawab 4,910) + chunk 06
               nafha-14 [259-261] (jawab 2,525) -> ONE item
               'jild28-shamama-4-nufha-14', pages [254-261] (8 pp.),
               jawab 7,435. Evidence: p. 258 ends mid-anecdote
               (Ghawth al-A'zam, Baghdad 511H, the sick man on the
               road) and p. 259 continues it. Net -1.
  shamama-4-nufha-21: 2 parts -> 1, RENAME-THEN-COMBINE. Lesson
               535, nafha 21 (Qahistani ki sharh Naqaya). Chunk 06
               nafha-21 [303] (jawab 491) + chunk 07 risala-535
               [304-334] (jawab 29,617) -> ONE item
               'jild28-shamama-4-nufha-21', pages [303-334] (32 pp.),
               jawab 30,108. Evidence: p. 303 has "wallahul
               musta'an wa lillahil hamd" closing nafha-20, then
               "nafha 21: qal al-Qahistani fi sharh al-Naqaya..."
               and p. 304 continues the same Qahistani commentary
               with no new heading. Chunk 07's 'jild28-risala-535-
               tatimma' [336-360] is NOT part of this combine —
               distinct appendix after the formal close (10 Shawwal
               1333H + signature) on p. 334 and the gap p. 335.
               Net -1.
  zulal-shubha-1-muqaddimat: 2 parts -> 1, RENAME-THEN-COMBINE.
               Lesson 77, al-Zalal al-Naqi, shubha awwal ke
               muqaddimat. Chunk 11 zulal-shubha-1-muqaddimat
               [531-544] (jawab 12,808) + chunk 12 zalal-nqi-1
               [545-550] (jawab 6,249) -> ONE item
               'jild28-zulal-shubha-1-muqaddimat', pages [531-550]
               (20 pp.), jawab 19,057. Evidence: p. 544 ends
               mid-sentence ("...to in ko door az kar") and p. 545
               continues it ("ba'ida..."). Net -1.
  zalal-nqi-radd-abu-ubayda: 2 parts -> 1, RENAME-THEN-COMBINE.
               Lesson 77, Abu Ubayda ke radd ki takmeel. Chunk 12
               zalal-nqi-radd-abu-ubayda [579-593] (jawab 14,590) +
               chunk 13 risala-77-shubha-1 [595-603] (jawab 8,832)
               -> ONE item 'jild28-zalal-nqi-radd-abu-ubayda',
               pages [579-603] EXCLUDING gap 594 (24 unique pages,
               NOT 25), jawab 23,422. Evidence: p. 593 ends
               mid-sentence ("phir is ke do jawab diye: pehla to
               wahi jo ulama ne ikhtiyar farmaya yani") and p. 595
               continues the first answer's text. Net -1.
After the combines: 94 - 5 = 89 items covering 636 unique pages.

RENAME-ONLY LIST (16 renames, NO combine — different sections that
share an id; Jild 4 precedent — earliest keeps the plain id):
Lesson 535 id unification: chunk 03 already holds the plain
'jild28-nafha-1..10' ids for a different lesson (533), so chunk
05/06's plain nafha ids must move to the 'jild28-shamama-4-nufha-N'
form (chunk 04's convention):
  Chunk 05: nafha-4 -> shamama-4-nufha-4; nafha-5 -> -5; nafha-6
  -> -6; nafha-7 -> -7; nafha-8 -> -8; nafha-9 -> -9; nafha-10
  -> -10; nafha-11 -> -11; nafha-12 -> -12; nafha-13 -> -13.
  Chunk 06: nafha-15 -> shamama-4-nufha-15; nafha-16 -> -16;
  nafha-17 -> -17; nafha-18 -> -18; nafha-19 -> -19; nafha-20
  -> -20.
(Chunk 05's nafha-3 and nafha-14 and chunk 06's nafha-14 and
nafha-21 renames are part of combines 1-3 above, not this list.)
No applied-in-chunk print-error renames in this jild. The merge
must NOT apply any renames beyond the 7 combine renames + these
16 rename-onlys (23 total). Do NOT normalise the spelling: chunk
02's 'jild28-nafhah-N' (with 'h') vs chunks 03/05/06's
'jild28-nafha-N' are distinct strings — no collision, do NOT
unify them.

EMPTY-JAWAB RULE: after the merge, exactly ZERO empty jawabs (0
at chunk level, 0 after merge). Empty sawal after merge: exactly
72 (all by design — risala sections with no question; each
combine merges two empty-sawal parts into one item).

DO-NOT-COMBINES: Chunk 02's nafhah-12 does NOT continue into
chunk 03 — the translator's split flag was a false alarm,
corrected by the coordinator: the Kashf al-Ghummah citation
completes on p. 112 (ends "ah" + full Urdu translation, covered
to the last word in chunk 02's tashreeh) and p. 113 opens cleanly
with "al-Shamama al-Thaniya min Sandal al-Fiqh / nafha 1". The
stale note in chunk 02's file was corrected by the coordinator.
NO merge action. Chunk 13's shubha-3 does NOT continue into
chunk 14's tadhyeel — the seventh reply's argument concludes on
p. 640 and p. 641 opens a NEW headed section ("tadhyeel iyak an
tazunna anna taqdim al-khabar..."). Chunk 14's
'jild28-zulal-tadhyeel' [641-651] is a SEPARATE item. NO merge
action. Chunk 09's 'jild28-masala-8' [428-431]: NO rename — no
other masala-8 exists anywhere in the volume (verified against
ALL chunk files: chunk 08 has masala-4, 5, 6-ta-10, 11; chunk 10
has 19-22). The plain id is safe. Chunk 07's
'jild28-risala-535-tatimma' [336-360] stays separate (see combine
3). Chunk 08's masala-11 [368-403] is one item (whole risala
Tard al-Afa'i, ends p. 403 "risala ... khatm hua"); chunk 10's
masala-22-doom is a separate item from masala-22 (printed
"awwal"/"doom", no invented number). Source gaps: 46 pages —
pp. 11-50 (40), 335, 355, 364, 490, 492, 594. PUA pages: 511
(single U+F06D ornament before a Quran quote, verse intact —
chunk 11); 568 (U+F06E x2) and 574 (U+F06B x1) — decorative
ornaments before Quran quotes, verses intact (chunk 12). U+FFFD
pages: 310, 317, 320, 327, 353, 357 (chunk 07). Flagged in notes
only, never reconstructed. Volume closes p. 686 with the risala
end ("risala al-Zalal al-Naqi min bahr sabqat al-atqa khatm
hua") and the note "jild 28 kitab al-Shita hissa som fazail o
manaqib ke unwan par ikhtitam pazeer hui; jild 29 kitab al-Shita
ke hissa chaharum se shuru hogi in sha Allah ta'ala" — recorded
in chunk 14's latifa-baqillani item. No separate khatima item.
First item 'jild28-pesh-lafz' [5-10], last item
'jild28-zulal-latifa-baqillani' [683-686].

SORT: merged items are sorted by start_page for the final file.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# result id -> list of selectors, in page order.
# Selector forms:
#   ('id', sid)            — every item with this id (1 or 2 halves)
#   ('id_start', sid, sp)  — the item with this id starting at page sp
COMBINES = {
    'jild28-shamama-4-nufha-3': [
        ('id', 'jild28-shamama-4-nufha-3'),
        ('id_start', 'jild28-nafha-3', 213),
    ],
    'jild28-shamama-4-nufha-14': [
        ('id', 'jild28-nafha-14'),
    ],
    'jild28-shamama-4-nufha-21': [
        ('id', 'jild28-nafha-21'),
        ('id', 'jild28-risala-535'),
    ],
    'jild28-zulal-shubha-1-muqaddimat': [
        ('id', 'jild28-zulal-shubha-1-muqaddimat'),
        ('id', 'jild28-zalal-nqi-1'),
    ],
    'jild28-zalal-nqi-radd-abu-ubayda': [
        ('id', 'jild28-zalal-nqi-radd-abu-ubayda'),
        ('id', 'jild28-risala-77-shubha-1'),
    ],
}

# Sawal handling per combined id (default: sawal from the first part,
# sorted by min page). All five combines have empty sawal on every
# part (risala sections, no question), so every combined sawal is 0.
SAWAL_RULES = {}

# Rename-onlys: (old_id, start_page, new_id). Scoped by start_page
# because nafha-4..10 exist twice (chunk 03 lesson 533 keeps the
# plain id; chunk 05 lesson 535 must move to the shamama-4-nufha-N
# form). Applied AFTER the combines (combine parts use the old ids).
# 16 renames; the 7 combine renames are implemented by the COMBINES
# table itself (the combined item carries the result id).
RENAMES = [
    ('jild28-nafha-4', 215, 'jild28-shamama-4-nufha-4'),
    ('jild28-nafha-5', 218, 'jild28-shamama-4-nufha-5'),
    ('jild28-nafha-6', 219, 'jild28-shamama-4-nufha-6'),
    ('jild28-nafha-7', 225, 'jild28-shamama-4-nufha-7'),
    ('jild28-nafha-8', 229, 'jild28-shamama-4-nufha-8'),
    ('jild28-nafha-9', 232, 'jild28-shamama-4-nufha-9'),
    ('jild28-nafha-10', 238, 'jild28-shamama-4-nufha-10'),
    ('jild28-nafha-11', 247, 'jild28-shamama-4-nufha-11'),
    ('jild28-nafha-12', 249, 'jild28-shamama-4-nufha-12'),
    ('jild28-nafha-13', 251, 'jild28-shamama-4-nufha-13'),
    ('jild28-nafha-15', 261, 'jild28-shamama-4-nufha-15'),
    ('jild28-nafha-16', 266, 'jild28-shamama-4-nufha-16'),
    ('jild28-nafha-17', 271, 'jild28-shamama-4-nufha-17'),
    ('jild28-nafha-18', 274, 'jild28-shamama-4-nufha-18'),
    ('jild28-nafha-19', 286, 'jild28-shamama-4-nufha-19'),
    ('jild28-nafha-20', 289, 'jild28-shamama-4-nufha-20'),
]

# No applied-in-chunk renames in this jild.
RENAMED_IN_CHUNK = []

# Expected pages for every combined item (spot-check anchors).
EXPECTED_COMBINED_PAGES = {
    'jild28-shamama-4-nufha-3': list(range(206, 216)),
    'jild28-shamama-4-nufha-14': list(range(254, 262)),
    'jild28-shamama-4-nufha-21': list(range(303, 335)),
    'jild28-zulal-shubha-1-muqaddimat': list(range(531, 551)),
    'jild28-zalal-nqi-radd-abu-ubayda': [p for p in range(579, 604) if p != 594],
}

# Expected sawal/jawab char counts for every combined item.
# shamama-4-nufha-3 jawab: 5,650 + 2,200 = 7,850
# shamama-4-nufha-14 jawab: 4,910 + 2,525 = 7,435
# shamama-4-nufha-21 jawab: 491 + 29,617 = 30,108
# zulal-shubha-1-muqaddimat jawab: 12,808 + 6,249 = 19,057
# zalal-nqi-radd-abu-ubayda jawab: 14,590 + 8,832 = 23,422
EXPECTED_COMBINED_TEXT = {
    'jild28-shamama-4-nufha-3': (0, 7850),
    'jild28-shamama-4-nufha-14': (0, 7435),
    'jild28-shamama-4-nufha-21': (0, 30108),
    'jild28-zulal-shubha-1-muqaddimat': (0, 19057),
    'jild28-zalal-nqi-radd-abu-ubayda': (0, 23422),
}

# Ids absorbed by the combines (must be gone after merging).
# nafha-14 (both halves), nafha-21, risala-535, zalal-nqi-1 and
# risala-77-shubha-1 are gone entirely. Chunk 05's nafha-3
# (start_page 213) is absorbed, but chunk 03's nafha-3 [120-122]
# KEEPS the plain id — it is checked separately, start_page-scoped.
ABSORBED = [
    'jild28-nafha-14',
    'jild28-nafha-21',
    'jild28-risala-535',
    'jild28-zalal-nqi-1',
    'jild28-risala-77-shubha-1',
]

# The only items allowed to keep an empty sawal after merging
# (all by design — risala sections with no question). 72 items.
EMPTY_SAWAL_ALLOWED = {
    'jild28-pesh-lafz',
    'jild28-shamaim-al-anbar-intro',
    'jild28-nafhah-1',
    'jild28-nafhah-2',
    'jild28-nafhah-3',
    'jild28-nafhah-4',
    'jild28-nafhah-5',
    'jild28-nafhah-6',
    'jild28-nafhah-7',
    'jild28-nafhah-8',
    'jild28-nafhah-9',
    'jild28-nafhah-10',
    'jild28-nafhah-11',
    'jild28-nafhah-12',
    'jild28-nafha-1',
    'jild28-nafha-2',
    'jild28-nafha-3',
    'jild28-nafha-4',
    'jild28-nafha-5',
    'jild28-nafha-6',
    'jild28-nafha-7',
    'jild28-nafha-8',
    'jild28-nafha-9',
    'jild28-nafha-10',
    'jild28-shamama-3-nufha-1',
    'jild28-shamama-3-nufha-2',
    'jild28-shamama-3-nufha-3',
    'jild28-shamama-4-intro',
    'jild28-shamama-4-nufha-1',
    'jild28-shamama-4-nufha-2',
    'jild28-shamama-4-nufha-3',
    'jild28-shamama-4-nufha-4',
    'jild28-shamama-4-nufha-5',
    'jild28-shamama-4-nufha-6',
    'jild28-shamama-4-nufha-7',
    'jild28-shamama-4-nufha-8',
    'jild28-shamama-4-nufha-9',
    'jild28-shamama-4-nufha-10',
    'jild28-shamama-4-nufha-11',
    'jild28-shamama-4-nufha-12',
    'jild28-shamama-4-nufha-13',
    'jild28-shamama-4-nufha-14',
    'jild28-shamama-4-nufha-15',
    'jild28-shamama-4-nufha-16',
    'jild28-shamama-4-nufha-17',
    'jild28-shamama-4-nufha-18',
    'jild28-shamama-4-nufha-19',
    'jild28-shamama-4-nufha-20',
    'jild28-shamama-4-nufha-21',
    'jild28-risala-535-tatimma',
    'jild28-deobandi-fatwa',
    'jild28-zulal-intro',
    'jild28-zulal-muqaddima-1',
    'jild28-zulal-muqaddima-2',
    'jild28-zulal-razi-dalil',
    'jild28-zulal-munaqasha-1',
    'jild28-zulal-munaqasha-2',
    'jild28-zulal-shubha-1-muqaddimat',
    'jild28-zalal-nqi-muqaddima-3',
    'jild28-zalal-nqi-muqaddima-4',
    'jild28-zalal-nqi-muqaddima-5',
    'jild28-zalal-nqi-talkhis',
    'jild28-zalal-nqi-radd-abu-ubayda',
    'jild28-zulal-tadhyeel',
    'jild28-zulal-takmeel',
    'jild28-zulal-tasjeel',
    'jild28-zulal-wajh-thani',
    'jild28-zulal-wajh-thalis',
    'jild28-zulal-tanbih',
    'jild28-zulal-khatima',
    'jild28-zulal-latifa-layl',
    'jild28-zulal-latifa-baqillani',
}

# After the merge, exactly ZERO empty jawabs.
EMPTY_JAWAB_ALLOWED = set()

# Chunk 03's plain nafha-1..10 (lesson 533) must keep their plain
# ids, with these exact pages.
KEPT_PLAIN_NAFHA = {
    'jild28-nafha-1': [113, 114, 115, 116, 117],
    'jild28-nafha-2': [117, 118, 119, 120],
    'jild28-nafha-3': [120, 121, 122],
    'jild28-nafha-4': [122, 123, 124],
    'jild28-nafha-5': [124, 125],
    'jild28-nafha-6': [125, 126, 127, 128, 129, 130, 131, 132],
    'jild28-nafha-7': [132, 133, 134],
    'jild28-nafha-8': [134, 135, 136],
    'jild28-nafha-9': [136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149],
    'jild28-nafha-10': [149, 150, 151, 152, 153, 154, 155],
}

# Chunk 02's nafhah-1..12 (with 'h') must stay untouched, with
# these exact pages. Do NOT normalise the spelling.
KEPT_NAFHAH = {
    'jild28-nafhah-1': list(range(65, 78)),
    'jild28-nafhah-2': [77, 78, 79],
    'jild28-nafhah-3': list(range(79, 89)),
    'jild28-nafhah-4': list(range(89, 94)),
    'jild28-nafhah-5': [93, 94, 95],
    'jild28-nafhah-6': [95, 96],
    'jild28-nafhah-7': [96, 97],
    'jild28-nafhah-8': [97, 98, 99],
    'jild28-nafhah-9': list(range(99, 105)),
    'jild28-nafhah-10': [104, 105],
    'jild28-nafhah-11': [105, 106, 107],
    'jild28-nafhah-12': list(range(107, 113)),
}

# The 16 rename-only targets, with their exact pages.
RENAMED_TARGETS = {
    'jild28-shamama-4-nufha-4': [215, 216, 217, 218],
    'jild28-shamama-4-nufha-5': [218, 219],
    'jild28-shamama-4-nufha-6': [219, 220, 221, 222, 223, 224, 225],
    'jild28-shamama-4-nufha-7': [225, 226, 227, 228, 229],
    'jild28-shamama-4-nufha-8': [229, 230, 231, 232],
    'jild28-shamama-4-nufha-9': [232, 233, 234, 235, 236, 237, 238],
    'jild28-shamama-4-nufha-10': [238, 239, 240, 241, 242, 243, 244, 245, 246, 247],
    'jild28-shamama-4-nufha-11': [247, 248, 249],
    'jild28-shamama-4-nufha-12': [249, 250, 251],
    'jild28-shamama-4-nufha-13': [251, 252, 253, 254],
    'jild28-shamama-4-nufha-15': [261, 262, 263, 264, 265, 266],
    'jild28-shamama-4-nufha-16': [266, 267, 268, 269, 270, 271],
    'jild28-shamama-4-nufha-17': [271, 272, 273],
    'jild28-shamama-4-nufha-18': [274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286],
    'jild28-shamama-4-nufha-19': [286, 287, 288, 289],
    'jild28-shamama-4-nufha-20': list(range(289, 304)),
}

# Items that must stay separate, with their exact pages.
KEPT_SEPARATE = {
    'jild28-risala-535-tatimma': [p for p in range(336, 361) if p != 355],
    'jild28-zulal-tadhyeel': list(range(641, 652)),
    'jild28-masala-8': [428, 429, 430, 431],
    'jild28-masala-11': list(range(368, 404)),
    'jild28-masala-22': list(range(469, 479)),
    'jild28-masala-22-doom': list(range(478, 490)),
    'jild28-pesh-lafz': [5, 6, 7, 8, 9, 10],
    'jild28-zulal-latifa-baqillani': [683, 684, 685, 686],
}


def combine_parts(result_id, parts):
    parts = sorted(parts, key=lambda it: min(it['pages']))
    first = parts[0]
    rule = SAWAL_RULES.get(result_id)
    if rule and rule[0] == 'concat':
        sawal = ''.join((parts[i].get('tashreeh_sawal', '') or '')
                        for i in rule[1])
    elif rule and rule[0] == 'from':
        sawal = parts[rule[1]].get('tashreeh_sawal', '') or ''
    else:
        sawal = first.get('tashreeh_sawal', '') or ''
    title = first.get('title') or ''
    combined = {
        'id': result_id,
        'title': title,
        'volume_id': 32,
        'pages': sorted(set().union(*[set(p['pages']) for p in parts])),
        'start_page': min(min(p['pages']) for p in parts),
        'tashreeh_sawal': sawal,
        'tashreeh_jawab': ''.join((p.get('tashreeh_jawab', '') or '') for p in parts),
        'notes': [n for p in parts for n in (p.get('notes') or [])],
    }
    return combined


def select_parts(all_items, selectors):
    """Resolve selectors to the matching items (each used at most once)."""
    parts = []
    used = set()
    for sel in selectors:
        if sel[0] == 'id':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and id(it) not in used]
        elif sel[0] == 'id_start':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and it['start_page'] == sel[2]
                    and id(it) not in used]
        else:
            raise ValueError(f'unknown selector {sel}')
        assert hits, f'no items matched selector {sel}'
        for it in hits:
            used.add(id(it))
        parts.extend(hits)
    return parts


def run_merge(manifest_path, base, write=False):
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    all_items = []
    merged_chunks = []
    for entry in manifest['chunks']:
        nn = entry['chunk']
        if entry.get('status') == 'split-halves':
            print(f'chunk {nn}: split-halves placeholder — halves are separate entries, skipping')
            continue
        # A chunk may be one file ("file") or split halves ("files").
        file_list = entry.get('files') or [entry['file']]
        items = []
        for fname in file_list:
            path = os.path.join(base, fname)
            if not os.path.exists(path):
                print(f'chunk {nn}: {fname} not yet written')
                continue
            try:
                d = json.load(open(path, encoding='utf-8'))
            except json.JSONDecodeError as e:
                # File may still be streaming from its translator; skip it
                # for now instead of crashing the whole merge.
                print(f'chunk {nn}: {fname} not valid JSON yet ({e}) — skipping for now')
                continue
            items.extend(d['masail'])
        if not items:
            print(f'chunk {nn}: no items loaded — skipping')
            continue
        # Normalize: some translators omit start_page; derive it from pages.
        for it in items:
            if 'start_page' not in it:
                assert it.get('pages'), f'chunk {nn} item {it.get("id")} has no pages'
                it['start_page'] = it['pages'][0]
                print(f'chunk {nn}: derived start_page={it["start_page"]} for {it["id"]}')
            assert it['start_page'] == min(it['pages']), \
                f'chunk {nn} item {it["id"]}: start_page != first page'
            it['_src_file'] = file_list[0]
        all_items.extend(items)
        merged_chunks.append(nn)
        entry['status'] = 'merged'
        print(f'chunk {nn}: {len(items)} items merged')
    print(f'items before combines: {len(all_items)}')
    assert len(all_items) == 94, f'expected 94 chunk items, got {len(all_items)}'
    # COMBINE the 5 cases.
    for result_id, selectors in COMBINES.items():
        parts = select_parts(all_items, selectors)
        combined = combine_parts(result_id, parts)
        assert combined['pages'] == EXPECTED_COMBINED_PAGES[result_id], \
            f'{result_id}: pages {combined["pages"][:3]}...{combined["pages"][-3:]} ({len(combined["pages"])} pp.) != expected {EXPECTED_COMBINED_PAGES[result_id][:3]}...{EXPECTED_COMBINED_PAGES[result_id][-3:]} ({len(EXPECTED_COMBINED_PAGES[result_id])} pp.)'
        exp_sawal, exp_jawab = EXPECTED_COMBINED_TEXT[result_id]
        assert len(combined['tashreeh_sawal']) == exp_sawal, \
            f'{result_id}: sawal {len(combined["tashreeh_sawal"])} chars != expected {exp_sawal}'
        assert len(combined['tashreeh_jawab']) == exp_jawab, \
            f'{result_id}: jawab {len(combined["tashreeh_jawab"])} chars != expected {exp_jawab}'
        assert combined['tashreeh_jawab'], f'{result_id}: combined jawab is empty!'
        if exp_sawal:
            assert combined['tashreeh_sawal'], f'{result_id}: combined sawal is empty!'
        assert combined['start_page'] == min(combined['pages']), f'{result_id}: start_page != min(pages)'
        used_ids = set(id(p) for p in parts)
        all_items = [it for it in all_items if id(it) not in used_ids]
        all_items.append(combined)
        print(f'COMBINED {result_id}: {len(parts)} parts, pages {combined["pages"][0]}-{combined["pages"][-1]} '
              f'({len(combined["pages"])} pages), sawal {len(combined["tashreeh_sawal"])} chars, '
              f'jawab {len(combined["tashreeh_jawab"])} chars, notes {len(combined["notes"])}')
    # RENAME-ONLY: 16 renames, scoped by start_page (nafha-4..10
    # exist twice: chunk 03 lesson 533 keeps the plain id).
    for old_id, start_page, new_id in RENAMES:
        assert not any(it['id'] == new_id for it in all_items), \
            f'rename target {new_id} already exists!'
        hits = [it for it in all_items
                if it['id'] == old_id and it['start_page'] == start_page]
        assert len(hits) == 1, \
            f'rename source {old_id} @ {start_page}: expected exactly 1 item, found {len(hits)}'
        hits[0]['id'] = new_id
        print(f'RENAMED {old_id} @ {start_page} -> {new_id} (pages {hits[0]["pages"][0]}-{hits[0]["pages"][-1]})')
    # Verify absorbed ids are gone (chunk 05's nafha-3 is checked
    # start_page-scoped below, since chunk 03's nafha-3 keeps the
    # plain id).
    for sid in ABSORBED:
        assert not any(it['id'] == sid for it in all_items), \
            f'absorbed id {sid} must not exist after combining!'
    assert not any(it['id'] == 'jild28-nafha-3' and it['start_page'] == 213
                   for it in all_items), \
        "chunk 05's jild28-nafha-3 [213-215] must not exist after combining!"
    print(f'absorbed ids gone: {len(ABSORBED)} + chunk-05 nafha-3')
    # Verify applied-in-chunk renames exist (none in this jild).
    for sid in RENAMED_IN_CHUNK:
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'applied-in-chunk id {sid}: expected exactly 1 item, found {len(hits)}'
    print(f'applied-in-chunk renames present: {RENAMED_IN_CHUNK}')
    # Verify the 16 rename-only targets exist with exact pages.
    for sid, exp_pages in RENAMED_TARGETS.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'rename target {sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'rename-only targets present: {len(RENAMED_TARGETS)}')
    # Chunk 03's plain nafha-1..10 (lesson 533) keep their plain ids.
    for sid, exp_pages in KEPT_PLAIN_NAFHA.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'{sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'chunk 03 plain nafha-1..10 kept: {len(KEPT_PLAIN_NAFHA)}')
    # Chunk 02's nafhah-1..12 (with 'h') stay untouched.
    for sid, exp_pages in KEPT_NAFHAH.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'{sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'chunk 02 nafhah-1..12 untouched: {len(KEPT_NAFHAH)}')
    # Items that must stay separate, with their exact pages.
    for sid, exp_pages in KEPT_SEPARATE.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'{sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'kept-separate items present: {len(KEPT_SEPARATE)}')
    ids = [it['id'] for it in all_items]
    assert len(ids) == len(set(ids)), f'STILL DUPLICATE IDS: {[i for i in ids if ids.count(i) > 1]}'
    empty = [it['id'] for it in all_items if not it.get('tashreeh_jawab')]
    assert set(empty) == EMPTY_JAWAB_ALLOWED, \
        f'EMPTY JAWAB mismatch: {sorted(empty)} != {sorted(EMPTY_JAWAB_ALLOWED)}'
    print(f'empty jawab: {sorted(empty)} (expected: none)')
    empty_sawal = [it['id'] for it in all_items if not it.get('tashreeh_sawal')]
    assert set(empty_sawal) == EMPTY_SAWAL_ALLOWED, \
        f'EMPTY SAWAL mismatch: {sorted(empty_sawal)} != {sorted(EMPTY_SAWAL_ALLOWED)}'
    print(f'empty sawal (by design only): {len(empty_sawal)} items')
    pages = set()
    for it in all_items:
        pages.update(it['pages'])
    # PRIMARY coverage check (Jild 17 lesson): validate against the
    # 636 unique pages directly, not against a range-minus-gaps
    # computation. Source gaps are pp. 11-50 (40), 335, 355, 364,
    # 490, 492, 594 (46 total, nothing invented).
    assert len(pages) == 636, f'expected 636 unique pages, got {len(pages)}'
    assert min(pages) == 5 and max(pages) == 686, \
        f'page span {min(pages)}-{max(pages)} != 5-686'
    # Secondary cross-check: per-chunk page range and item count must
    # equal the manifest's values for that chunk. (This manifest uses
    # 'pages' for the [first, last] page range and 'items' for the
    # item count; combined items carry pages from several chunks, so
    # per-chunk attribution must come from the raw file, not from the
    # merged items.)
    for entry in manifest['chunks']:
        if entry['chunk'] in merged_chunks:
            d = json.load(open(os.path.join(base, entry['file']), encoding='utf-8'))
            raw_pages = set()
            for it in d['masail']:
                raw_pages.update(it['pages'])
            assert min(raw_pages) == entry['pages'][0] and max(raw_pages) == entry['pages'][1], \
                f'chunk {entry["chunk"]}: page span {min(raw_pages)}-{max(raw_pages)} != manifest {entry["pages"]}'
            assert len(d['masail']) == entry['items'], \
                f'chunk {entry["chunk"]}: {len(d["masail"])} items != manifest {entry["items"]}'
    print(f'total items: {len(all_items)} | pages covered: {len(pages)}')
    assert len(all_items) == 89, f'expected 89 items after combines, got {len(all_items)}'
    # sort by start_page for the final file
    all_items.sort(key=lambda it: it['start_page'])
    for it in all_items:
        it.pop('_src_file', None)
    if write:
        with open(os.path.join(base, 'jild-28.json'), 'w', encoding='utf-8') as f:
            json.dump({'masail': all_items}, f, ensure_ascii=False, indent=1)
        with open(os.path.join(base, 'chunks-manifest-jild28.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'WROTE jild-28.json: {len(all_items)} items, {len(pages)} pages, chunks merged: {merged_chunks}')
    return all_items, pages, merged_chunks


def main():
    manifest_path = os.path.join(BASE, 'chunks-manifest-jild28.json')
    run_merge(manifest_path, BASE, write=True)


if __name__ == '__main__':
    main()
