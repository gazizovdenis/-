import re

html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

FEP = "https://www.fashioneyewear.com/cdn/shop/products/"
FEF = "https://www.fashioneyewear.com/cdn/shop/files/"

# key: partial substring of img src → (new_src_or_None, [extra1, extra2])
# new_src = None: keep current img src, only add gallery extras
CARDS = {
    # ── RB3025 AVIATOR ──────────────────────────────────────────────────
    "p_aviator.jpg": (None, [
        FEP + "0RB3025__9196G5_000A_1800x1800.jpg",
        FEP + "0RB3025__9196G5_090A_1800x1800.jpg",
    ]),
    "01e9f4b618e5c89905f194b3c6b17429": (None, [   # eye-oo Silver/Grey Mirror
        FEP + "0rb3025__112_m2_000a_1800x1800.jpg",
        FEP + "0rb3025__112_m2_090a_1800x1800.jpg",
    ]),
    # ChatGPT → replace + gallery
    "10_13_28 (1).png": (
        FEP + "0rb3025__001_030a_converted_22343_1800x1800.jpg",
        [FEP + "0rb3025__001_000a_converted_22343_1800x1800.jpg",
         FEP + "0rb3025__001_090a_converted_22343_1800x1800.jpg"]),
    "10_13_28 (2).png": (
        FEP + "0RB3025__9196G6_030A_1800x1800.jpg",
        [FEP + "0RB3025__9196G6_000A_1800x1800.jpg",
         FEP + "0RB3025__9196G6_090A_1800x1800.jpg"]),
    "10_13_28 (3).png": (
        FEP + "0rb3025__112_19_030a_1_converted_22400_1800x1800.jpg",
        [FEP + "0rb3025__112_19_000a_1_converted_22400_1800x1800.jpg",
         FEP + "0rb3025__112_19_090a_1_converted_22400_1800x1800.jpg"]),
    "10_13_29 (4).png": (
        FEP + "0rb3025__004_58_030a_1800x1800.jpg",
        [FEP + "0rb3025__004_58_000a_1800x1800.jpg",
         FEP + "0rb3025__004_58_090a_1800x1800.jpg"]),
    "10_21_59 (1).png": (
        FEP + "0rb3025__001_3e_030a_1800x1800.jpg",
        [FEP + "0rb3025__001_3e_000a_1800x1800.jpg",
         FEP + "0rb3025__001_3e_090a_1800x1800.jpg"]),

    # ── RB3026 AVIATOR LARGE ─────────────────────────────────────────────
    "p_aviator_large2.jpg": (None, [
        FEP + "luxbs0rb3026__l2846_000a.jpg",
        FEP + "luxbs0rb3026__l2846_090a.jpg",
    ]),

    # ── RB2140 WAYFARER ──────────────────────────────────────────────────
    "p2_wayfarer_black.jpg": (
        FEP + "luxbs0rb2140__901_030a.jpg",
        [FEP + "luxbs0rb2140__901_000a.jpg", FEP + "luxbs0rb2140__901_090a.jpg"]),
    "p3_wayfarer_tortoise.jpg": (
        FEP + "luxbs0rb2140__902_030a.jpg",
        [FEP + "luxbs0rb2140__902_000a.jpg", FEP + "luxbs0rb2140__902_090a.jpg"]),
    "p1_wayfarer_transparent.jpg": (None, [          # keep Transparent Red, add Blue proxy angles
        FEP + "0rb2140__13193f_000a.jpg",
        FEP + "0rb2140__13193f_090a.jpg",
    ]),
    "3d2db673629c6d8acd87475befc2dcf7": (None, [     # eye-oo Transparent Violet
        FEP + "0RB2140__1333G6_000A.jpg",
        FEP + "0RB2140__1333G6_090A.jpg",
    ]),
    "1334G3_030A_ccc1031a": (None, [                 # FE hash Transparent Pink Polar.
        FEF + "0RB2140__1334G3_000A_2929112a-d7a2-462c-9b2e-ed851a3997c7.jpg",
        FEF + "0RB2140__1334G3_090A_651d3bec-6018-4eb7-9755-896991a58436.jpg",
    ]),
    "6615B1_030A": (None, [                          # FE hash Transparent Green (proxy)
        FEP + "0rb2140__13193f_000a.jpg",
        FEP + "0rb2140__13193f_090a.jpg",
    ]),
    # ChatGPT Wayfarer → replace + gallery
    "09_25_33 (1).png": (
        FEP + "0RB2140__1292B1_030A.jpg",
        [FEP + "0RB2140__1292B1_000A.jpg", FEP + "0RB2140__1292B1_090A.jpg"]),
    "09_25_33 (2).png": (
        FEP + "0RB2140__1333G6_030A.jpg",
        [FEP + "0RB2140__1333G6_000A.jpg", FEP + "0RB2140__1333G6_090A.jpg"]),
    "09_25_33 (3).png": (
        FEP + "0rb2140__13193f_030a.jpg",
        [FEP + "0rb2140__13193f_000a.jpg", FEP + "0rb2140__13193f_090a.jpg"]),
    "09_25_33 (4).png": (
        FEP + "0RB2140__1332G5_030A.jpg",
        [FEP + "0RB2140__1332G5_000A.jpg", FEP + "0RB2140__1332G5_090A.jpg"]),
    "09_34_21 (1).png": (
        FEP + "0rb2140__902_51_030a_converted_23175.jpg",
        [FEP + "0rb2140__902_51_000a_converted_23175.jpg",
         FEP + "0rb2140__902_51_090a_converted_23175.jpg"]),
    "09_43_56 (3).png": (
        FEP + "0rb2140__13183a_030a.jpg",
        [FEP + "0rb2140__13183a_000a.jpg", FEP + "0rb2140__13183a_090a.jpg"]),
    "10_19_22 (1).png": (                            # Wayfarer Blue/Blue Classic
        FEP + "0rb2140__13193f_030a.jpg",
        [FEP + "0rb2140__13193f_000a.jpg", FEP + "0rb2140__13193f_090a.jpg"]),
    "10_19_23 (3).png": (                            # Wayfarer Transparent Orange
        FEP + "0RB2140__1292B1_030A.jpg",
        [FEP + "0RB2140__1292B1_000A.jpg", FEP + "0RB2140__1292B1_090A.jpg"]),
    "11_50_20 (5).png": (
        FEP + "0rb2140__902_51_030a_converted_23175.jpg",
        [FEP + "0rb2140__902_51_000a_converted_23175.jpg",
         FEP + "0rb2140__902_51_090a_converted_23175.jpg"]),

    # ── RBR0502S WAYFARER REVERSE ────────────────────────────────────────
    "p6_reverse_r0502s_a.jpg": (None, [
        FEF + "0RBR0502S__6677VR_000A_73d28efd-3118-4ff5-b8ab-286ff564149e.jpg",
        FEF + "0RBR0502S__6677VR_090A_dded70f3-f8c4-4cb4-b35f-b24019385fa2.jpg",
    ]),
    "p7_reverse_r0502s_b.jpg": (None, [
        FEF + "0RBR0502S__67083A_000A_2ae393be-95a8-48a6-9160-e9ad9b717e71.jpg",
        FEF + "0RBR0502S__67083A_090A_9d41761e-31ac-4d38-aea3-cb9cc6682ffa.jpg",
    ]),
    "6677VR_030A_7621c0d3": (None, [
        FEF + "0RBR0502S__6677VR_000A_73d28efd-3118-4ff5-b8ab-286ff564149e.jpg",
        FEF + "0RBR0502S__6677VR_090A_dded70f3-f8c4-4cb4-b35f-b24019385fa2.jpg",
    ]),
    "6712GM_030A_e9772b36": (None, [
        FEF + "0RBR0502S__6712GM_000A_af4d2fca-b003-4e83-8b77-e9a09fae4626.jpg",
        FEF + "0RBR0502S__6712GM_090A_f22abbe9-e982-4828-929f-f1ee2ff1c610.jpg",
    ]),
    "6790VR__P21__shad__qt_2553c8c2": (None, [
        FEF + "0RBR0502S__6790VR__P21__shad__fr_2b895ae6-5cbc-4864-86b1-ce35e4547af8.jpg",
        FEF + "0RBR0502S__6790VR__P21__shad__lt_59769664-ea33-4f2f-93e1-7b1edf9423c6.jpg",
    ]),
    "678072__P21__shad__qt_7c771846": (None, [
        FEF + "0RBR0502S__678072__P21__shad__fr_36c07dd8-73a8-4b49-a8f1-3389d0411749.jpg",
        FEF + "0RBR0502S__678072__P21__shad__lt_e8ce3058-913d-445e-80cc-7fcc3f989f89.jpg",
    ]),
    "667772__P21__shad__qt_7f641e24": (None, [
        FEF + "0RBR0502S__667772__P21__shad__fr_5c0feabc-39fb-4d50-a7db-87a1b6e41c2b.jpg",
        FEF + "0RBR0502S__667772__P21__shad__lt_397107a8-e4e5-49a1-8717-8c4b5ef71020.jpg",
    ]),
    "66771A__P21__shad__qt_4d64efa3": (None, [
        FEF + "0RBR0502S__66771A__P21__shad__fr_20d655f3-7767-4d77-9248-3d8845cb21ec.jpg",
        FEF + "0RBR0502S__66771A__P21__shad__lt_53da6a7f-ae6c-411e-827e-aafafd162e51.jpg",
    ]),
    "679183__P21__shad__qt_a8ede24e": (None, [
        FEF + "0RBR0502S__679183__P21__shad__fr_b6911c48-1fc3-43e5-9fae-7a24c1afde4c.jpg",
        FEF + "0RBR0502S__679183__P21__shad__lt_099d9c7f-9623-4d62-8e37-a23d531ff6b9.jpg",
    ]),

    # ── RBR0501S BOYFRIEND REVERSE ───────────────────────────────────────
    "rbr0501s-6677vr-00": (None, [
        FEF + "0RBR0502S__6677VR_000A_73d28efd-3118-4ff5-b8ab-286ff564149e.jpg",
        FEF + "0RBR0502S__6677VR_090A_dded70f3-f8c4-4cb4-b35f-b24019385fa2.jpg",
    ]),
    "rbr0501s-6707gs-00": (None, [
        FEF + "0RBR0502S__6707GR_000A_d058dafe-30fc-47bb-86ca-2b993b0197e1.jpg",
        FEF + "0RBR0502S__6707GR_090A_f065eec1-39c8-4412-94ae-de569739fb9d.jpg",
    ]),
    "0RBR0501S__6790VR__P21__shad__fr": (None, [
        FEF + "0RBR0502S__6790VR__P21__shad__fr_2b895ae6-5cbc-4864-86b1-ce35e4547af8.jpg",
        FEF + "0RBR0502S__6790VR__P21__shad__lt_59769664-ea33-4f2f-93e1-7b1edf9423c6.jpg",
    ]),
    "rb_0rbr0501s_0rbr0501s__67083a": (None, [
        FEF + "0RBR0502S__67083A_000A_2ae393be-95a8-48a6-9160-e9ad9b717e71.jpg",
        FEF + "0RBR0502S__67083A_090A_9d41761e-31ac-4d38-aea3-cb9cc6682ffa.jpg",
    ]),

    # ── RBR0101S AVIATOR REVERSE ─────────────────────────────────────────
    "002_GS_030A_28ffc9a0": (None, [
        FEF + "0RBR0101S__002_GS_000A_b5cf1ba7-5b5e-479a-a6fd-21fae84a9109.jpg",
        FEF + "0RBR0101S__002_GS_090A_8d8415a6-1dc2-4856-a326-561330001b9c.jpg",
    ]),
    "001_82__P21__shad__qt_43ef6773": (None, [
        FEF + "0RBR0101S__001_82__P21__shad__fr_c93ce968-f069-481d-bf5a-becc8ce5e518.jpg",
        FEF + "0RBR0101S__001_82__P21__shad__lt_52f6d6c3-e018-4cb2-a704-ea8a3e2a8605.jpg",
    ]),
    "002_GR__P21__shad__qt_e84a60ad": (None, [
        FEF + "0RBR0101S__002_GR__P21__shad__fr_fe382193-0a26-43f3-99b9-f54fc1de6d57.jpg",
        FEF + "0RBR0101S__002_GR__P21__shad__lt_669b4937-ed7f-496b-9c6a-60c45c159acd.jpg",
    ]),
    "003_GR_030A_18878311": (None, [
        FEF + "0RBR0101S__003_GR_000A_635db649-21da-4bd2-8dfe-e17dbab363b0.jpg",
        FEF + "0RBR0101S__003_GR_090A_044a419f-95cb-4a36-92cf-be11d266cab2.jpg",
    ]),
    "004_CB_030A_5df786e5": (None, [
        FEF + "0RBR0101S__004_CB_000A_b0094d3b-4985-4784-b80f-817d8311d96a.jpg",
        FEF + "0RBR0101S__004_CB_090A_744423ca-9c41-4142-989c-9d57a091ddda.jpg",
    ]),
    "92023A_030A_feabdfd7": (None, [
        FEF + "0RBR0101S__92023A_000A_09b6aeef-09a2-47a6-845d-30c7ea8bb3b5.jpg",
        FEF + "0RBR0101S__92023A_090A_a5fbcf97-d86b-42cb-b46c-ef11844464bb.jpg",
    ]),
    "11a5c5f1e769717d2f5baa3eb7eff58b": (None, [    # eye-oo Silver/Light Blue Mirror proxy
        FEF + "0RBR0101S__003_GR_000A_635db649-21da-4bd2-8dfe-e17dbab363b0.jpg",
        FEF + "0RBR0101S__003_GR_090A_044a419f-95cb-4a36-92cf-be11d266cab2.jpg",
    ]),

    # ── RBR0102S CARAVAN REVERSE ─────────────────────────────────────────
    "39675d7145c6576597d1a0ef1d7acc34": (None, [    # eye-oo Gold/Green proxy
        FEF + "0RBR0103S__001_VR__P21__shad__fr_0f12521c-45f4-45f1-8e95-d05099ce57b9.jpg",
        FEF + "0RBR0103S__001_VR__P21__shad__lt_8c8a2155-0135-4ae2-b3e6-4cc70d913934.jpg",
    ]),
    "p10_caravan_reverse.jpg": (None, [
        FEF + "0RBR0103S__002_GR__P21__shad__fr_819bcdca-8b71-472a-bd31-0498c277d120.jpg",
        FEF + "0RBR0103S__002_GR__P21__shad__lt_bf76b62a-c31b-42ed-9f07-6158a8982cb6.jpg",
    ]),

    # ── RBR0103S ROUND REVERSE ───────────────────────────────────────────
    "001_VR__P21__shad__qt_60e54de8": (None, [
        FEF + "0RBR0103S__001_VR__P21__shad__fr_0f12521c-45f4-45f1-8e95-d05099ce57b9.jpg",
        FEF + "0RBR0103S__001_VR__P21__shad__lt_8c8a2155-0135-4ae2-b3e6-4cc70d913934.jpg",
    ]),
    "002_GR__P21__shad__qt_0db6418f": (None, [
        FEF + "0RBR0103S__002_GR__P21__shad__fr_819bcdca-8b71-472a-bd31-0498c277d120.jpg",
        FEF + "0RBR0103S__002_GR__P21__shad__lt_bf76b62a-c31b-42ed-9f07-6158a8982cb6.jpg",
    ]),
    "92023A__P21__shad__qt_60fc262e": (None, [      # Rose Gold/Dark Blue proxy
        FEF + "0RBR0103S__001_VR__P21__shad__fr_0f12521c-45f4-45f1-8e95-d05099ce57b9.jpg",
        FEF + "0RBR0103S__001_VR__P21__shad__lt_8c8a2155-0135-4ae2-b3e6-4cc70d913934.jpg",
    ]),
    "001_CB__P21__shad__qt_fb04942c": (None, [
        FEF + "0RBR0103S__001_VR__P21__shad__fr_0f12521c-45f4-45f1-8e95-d05099ce57b9.jpg",
        FEF + "0RBR0103S__001_VR__P21__shad__lt_8c8a2155-0135-4ae2-b3e6-4cc70d913934.jpg",
    ]),
    "001_83__P21__shad__qt_cd2aaf47": (None, [
        FEF + "0RBR0103S__001_VR__P21__shad__fr_0f12521c-45f4-45f1-8e95-d05099ce57b9.jpg",
        FEF + "0RBR0103S__001_VR__P21__shad__lt_8c8a2155-0135-4ae2-b3e6-4cc70d913934.jpg",
    ]),
    "004_9A__P21__shad__qt_8105dce8": (None, [
        FEF + "0RBR0103S__002_GR__P21__shad__fr_819bcdca-8b71-472a-bd31-0498c277d120.jpg",
        FEF + "0RBR0103S__002_GR__P21__shad__lt_bf76b62a-c31b-42ed-9f07-6158a8982cb6.jpg",
    ]),

    # ── RB2132 NEW WAYFARER ──────────────────────────────────────────────
    "10_19_23 (4).png": (
        FEP + "luxbs0rb2132__622_030a.jpg",
        [FEP + "luxbs0rb2132__622_000a.jpg", FEP + "luxbs0rb2132__622_090a.jpg"]),
    "10_19_23 (5).png": (
        FEP + "luxbs0rb2132__901_030a.jpg",
        [FEP + "luxbs0rb2132__901_000a.jpg", FEP + "luxbs0rb2132__901_090a.jpg"]),
    "10_19_23 (6).png": (
        FEP + "0rb2132__710_030a.jpg",
        [FEP + "0rb2132__710_000a.jpg", FEP + "0rb2132__710_090a.jpg"]),

    # ── RB0840S MEGA WAYFARER ────────────────────────────────────────────
    "09_54_28 (1).png": (
        FEP + "0RB0840S__668073_030A.jpg",
        [FEP + "0RB0840S__668073_000A.jpg", FEP + "0RB0840S__668073_090A.jpg"]),
    "09_54_28 (2).png": (
        FEP + "0RB0840S__901_31_030A.jpg",
        [FEP + "0RB0840S__901_31_000A.jpg", FEP + "0RB0840S__901_31_090A.jpg"]),
    "09_54_28 (3).png": (
        FEP + "0RB0840S__668073_030A.jpg",
        [FEP + "0RB0840S__668073_000A.jpg", FEP + "0RB0840S__668073_090A.jpg"]),
    "09_54_28 (4).png": (
        FEP + "0RB0840S__668073_030A.jpg",
        [FEP + "0RB0840S__668073_000A.jpg", FEP + "0RB0840S__668073_090A.jpg"]),
    "09_54_29 (5).png": (
        FEP + "0RB0840S__901_31_030A.jpg",
        [FEP + "0RB0840S__901_31_000A.jpg", FEP + "0RB0840S__901_31_090A.jpg"]),
    "09_54_29 (6).png": (
        FEP + "0RB0840S__901_31_030A.jpg",
        [FEP + "0RB0840S__901_31_000A.jpg", FEP + "0RB0840S__901_31_090A.jpg"]),
    "09_54_29 (7).png": (
        FEP + "0RB0840S__668073_030A.jpg",
        [FEP + "0RB0840S__668073_000A.jpg", FEP + "0RB0840S__668073_090A.jpg"]),
    "09_54_29 (8).png": (
        FEP + "0RB0840S__901_31_030A.jpg",
        [FEP + "0RB0840S__901_31_000A.jpg", FEP + "0RB0840S__901_31_090A.jpg"]),
    "09_54_30 (10).png": (
        FEP + "0RB0840S__668073_030A.jpg",
        [FEP + "0RB0840S__668073_000A.jpg", FEP + "0RB0840S__668073_090A.jpg"]),

    # ── RB3447 ROUND METAL ───────────────────────────────────────────────
    "9202R5_030A_c4f238ad": (None, [
        FEP + "luxbs0rb3447__001_000a.jpg",
        FEP + "luxbs0rb3447__001_090a.jpg",
    ]),
    "001_51_030A_0686b5e4": (None, [
        FEP + "luxbs0rb3447__001_000a.jpg",
        FEP + "luxbs0rb3447__001_090a.jpg",
    ]),
}


def get_auto_extras(src):
    """Auto-derive gallery extras for pretavoir/FE hd-1 and FE non-hash _030A patterns."""
    # hd-1 pattern (pretavoir.us or fashioneyewear.com)
    if 'hd-1.' in src:
        return [src.replace('hd-1.', 'hd-2.'), src.replace('hd-1.', 'hd-3.')]
    # FE non-hash _030A/_030a
    if 'fashioneyewear.com' in src:
        m = re.search(r'_030([Aa])', src)
        if m:
            idx = m.start()
            after = src[idx + 5:]
            # hash-based if after starts with _[hex]{8}-
            if re.match(r'_[a-f0-9]{8}-', after):
                return []
            a = m.group(1)
            return [
                src[:idx] + f'_000{a}' + after,
                src[:idx] + f'_090{a}' + after,
            ]
    return []


def make_gallery(img_tag, new_src, extras):
    """Wrap img_tag in .card-gallery with extra images and nav dots."""
    # Build main img with class="active" and optionally new src
    main = img_tag.replace('<img ', '<img class="active" ', 1)
    if new_src:
        main = re.sub(r'src="[^"]+"', f'src="{new_src}"', main)

    extra_imgs = '\n'.join(f'<img loading="eager" src="{e}" alt="">' for e in extras)

    n = len(extras) + 1
    dots = ''.join(
        f'<span class="gallery-dot{" active" if i == 0 else ""}" data-idx="{i}"></span>'
        for i in range(n)
    )

    return (f'<div class="card-gallery">\n'
            f'{main}\n'
            f'{extra_imgs}\n'
            f'<div class="gallery-nav">{dots}</div>\n'
            f'</div>')


# ═══════════════════════════════════════════════════════════════════════════
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. CSS ─────────────────────────────────────────────────────────────────
gallery_css = """
        .card-gallery { position: relative; overflow: hidden; }
        .card-gallery img { display: none; width: 100%; }
        .card-gallery img.active { display: block; }
        .gallery-nav { position: absolute; bottom: 7px; left: 0; right: 0; display: flex; justify-content: center; gap: 5px; pointer-events: none; }
        .gallery-dot { width: 5px; height: 5px; border-radius: 50%; background: rgba(255,255,255,0.4); cursor: pointer; pointer-events: all; transition: background .15s; }
        .gallery-dot.active { background: rgba(255,255,255,0.92); }"""
mobile_css = "\n            .gallery-dot { width: 4px; height: 4px; gap: 4px; }"

style_end = html.rfind('</style>')
if '.card-gallery' not in html and style_end != -1:
    html = html[:style_end] + gallery_css + '\n    ' + html[style_end:]
    print("CSS added")

mobile_anchor = '            .card-specs { font-size: 8px; }'
if '.gallery-dot { width: 4px' not in html and mobile_anchor in html:
    html = html.replace(mobile_anchor, mobile_anchor + mobile_css)
    print("CSS mobile added")

# ── 2. Transform cards in Ray-Ban section ──────────────────────────────────
rb_start = html.find('<div class="brand-section" id="ray-ban">')
rb_end = html.find('<div class="brand-section" id="gucci">')
if rb_start == -1 or rb_end == -1:
    print("ERROR: Ray-Ban or Gucci section not found!")
    exit(1)

rb_section = html[rb_start:rb_end]
img_pat = re.compile(r'<img loading="lazy" src="([^"]+)" alt="([^"]*)">')

matches = list(img_pat.finditer(rb_section))
matches.reverse()  # right-to-left to preserve positions

transformed = 0
new_rb = rb_section

for m in matches:
    src = m.group(1)
    alt = m.group(2)

    # Skip if already wrapped
    pre = rb_section[max(0, m.start() - 60):m.start()]
    if 'card-gallery' in pre:
        continue

    new_src = None
    extras = []

    for key, val in CARDS.items():
        if key in src:
            cand_src, extras = val
            if cand_src:
                new_src = cand_src
            break

    if not extras:
        extras = get_auto_extras(src)

    if not extras:
        continue

    gallery_html = make_gallery(m.group(0), new_src, extras)
    new_rb = new_rb[:m.start()] + gallery_html + new_rb[m.end():]
    transformed += 1
    label = alt[:55] if alt else src[:55]
    print(f"  + {label}")

html = html[:rb_start] + new_rb + html[rb_end:]
print(f"\nTransformed: {transformed} cards")

# ── 3. JS ──────────────────────────────────────────────────────────────────
gallery_js = """
// ── Gallery ──
document.querySelectorAll('.gallery-dot').forEach(function(dot) {
  dot.addEventListener('click', function(e) {
    e.preventDefault(); e.stopPropagation();
    var nav = this.parentElement;
    var gal = nav.parentElement;
    var idx = parseInt(this.dataset.idx);
    gal.querySelectorAll('img').forEach(function(img, i) {
      img.classList.toggle('active', i === idx);
    });
    nav.querySelectorAll('.gallery-dot').forEach(function(d, i) {
      d.classList.toggle('active', i === idx);
    });
  });
});
document.querySelectorAll('.card-gallery').forEach(function(gal) {
  var sx = 0;
  gal.addEventListener('touchstart', function(e) {
    sx = e.touches[0].clientX;
  }, {passive: true});
  gal.addEventListener('touchend', function(e) {
    var dx = e.changedTouches[0].clientX - sx;
    if (Math.abs(dx) < 30) return;
    e.preventDefault(); e.stopPropagation();
    var imgs = gal.querySelectorAll('img');
    var dots = gal.querySelectorAll('.gallery-dot');
    var cur = 0;
    imgs.forEach(function(img, i) { if (img.classList.contains('active')) cur = i; });
    var next = dx < 0 ? Math.min(cur + 1, imgs.length - 1) : Math.max(cur - 1, 0);
    if (next === cur) return;
    imgs.forEach(function(img, i) { img.classList.toggle('active', i === next); });
    dots.forEach(function(d, i) { d.classList.toggle('active', i === next); });
  });
});
"""

if '// ── Gallery ──' not in html:
    last_script = html.rfind('</script>')
    if last_script != -1:
        html = html[:last_script] + gallery_js + html[last_script:]
        print("JS added")
    else:
        print("WARNING: </script> not found!")

# ── 4. Save ────────────────────────────────────────────────────────────────
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved.")
