import logging
import os
from typing import Dict, List, Optional, Tuple, TypedDict

import discord
from discord.ext import commands

BR_SCHEDULE = "\n".join(
    [
        "┌─────────┬──────────┬────────────┐",
        "│ Неделя  │ Макс. БР │ Период     │",
        "├─────────┼──────────┼────────────┤",
        "│ 1       │ 9.0      │ 01.09-07.09 │",
        "│ 2       │ 9.3      │ 08.09-14.09 │",
        "│ 3       │ 9.7      │ 15.09-21.09 │",
        "│ 4       │ 10.0     │ 22.09-28.09 │",
        "│ 5       │ 10.3     │ 29.09-05.10 │",
        "│ 6       │ 10.7     │ 06.10-12.10 │",
        "│ Last    │ 5.0      │ 13.10-19.10 │",
        "└─────────┴──────────┴────────────┘",
    ]
)

HELP_MESSAGE = (
    "Привет! Чтобы получить список техники и расписание БР, воспользуйтесь командой `/br`."
)

FOOTER_TEXT = "Система учета •KSML•"
MAIN_EMBED_COLOR = discord.Color(0x2B2D31)

EMPTY_ARROW = "👉 \u200B"

AIR_BR_DATA: Dict[str, BRInfo] = {
    "12.7": {
        "title": "12.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[ F-15E ]`, `F-16C`, *(F-15C)*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *(Su-27SM)*, **Su-25SM3**"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 `Jas-39C`"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *(F-15J(M))*, `Jas-39C`, `{ F-2A }`"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 J-10A, J-11A"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `Jas-39EBS`"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *(F-16AM)*, `Mirage 2000D-RMV`"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `Jas-39C`"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 `[ F-15I ]`, F-16C, F-16D"],
            },
        ],
    },
    "12.0": {
        "title": "12.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "👉 `(AV-8B Plus)`, `F-16A`, `A-10C`, `F-15A`, `F/A-18A`, F-16A ADF",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 `(F-4F KWS LV)`, *(MiG-29G)*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *(Су-33)*, *(Су-27)*, *(Як-141)*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "👉 *Harrier GR.7*, `MiG-21 Bison`, *(Sea Harrier FA 2)*, Tornado F.3 Late",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 `F-16AJ`, *F-15J*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 `F-16A MLU`, *(JH-7A)*, *(J-11)*, *(J-8F)*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `(AV-8B Plus)`, `(F-16A)`, F-16A ADF"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 `F-16A`"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `[JAS39A]`, *(JA37D)*"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *(Netz)*, Baz"],
            },
        ],
    },
    "11.7": {
        "title": "11.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `(AV-8B (NA))`, `(A-10C)`"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *MiG-29*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *(Як-141)*, МиГ-29"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 `(MiG-21 Bison)`, *(Sea Harrier FA 2)*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 *(JH-7A)*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 MiG-29 Sniper"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 **Mirage 2000D-R1**"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [EMPTY_ARROW],
            },
        ],
    },
    "11.3": {
        "title": "11.3",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 `F-5E FCU`"],
            },
            {
                "name": "🇨🇳 China",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *(Mirage 2000D-R1)*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [EMPTY_ARROW],
            },
        ],
    },
    "11.0": {
        "title": "11.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[A-10A Late]`, `[A-7K]`, `A-6E TRAM`, **F-4S**"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *Su-22M4*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[Су-25М]`, `Су-17М4`, `МиГ-27М`"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 *(Sea Harrier FRS.1)*, Jaguar IS"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *(AV-8S Late)*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 Q-5L, J-7D"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 *(AMX)*, **F-104S**"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 `(Super Etendard)`"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `(F-5A(G))`, `(AJS37)`, JA37C"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *(Kfir C.2)*"],
            },
        ],
    },
    "10.7": {
        "title": "10.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[A-10A Late]`, `[A-7E]`, `(A-6E TRAM)`, `A-7D`, **F-5A/C**"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *(MiG-21bis-SAU / \"Lazur-M\")*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *(Су-25 / К)*, *(МиГ-21бис)*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 *(Sea Harrier FRS.1)*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 `[A-7E]`, *(AV-8S Late)*, **F-5A**"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 *(F-5A)*, J-8B, *(Q-5L)*, *(J-7D)*, J-7E"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 *(MiG-21bis-SAU)*"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *(Mirage IIIE)*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `[F-5A(G)]`, `(AJ37)`, `{Saab F-35}`, *(MiG-21bis)*, J35XS"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *(Kfir Canard)*"],
            },
        ],
    },
    "10.3": {
        "title": "10.3",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[A-10A]`, *(A-7D)*, *(F-5A/C)*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 **F-4F**, *(MiG-21bis-SAU / \"Lazur-M\")*, `{Mirage IIIS C.70}`"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[Су-25 / K]`, *(МиГ-21бис)*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 *(Sea Harrier FRS.1 (e))*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *(F-5A)*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 `[Q-5L]`, *(J-7D)*, J-7E"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 *(MiG-21bis-SAU)*"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 `[NF-5A]`, *(Mirage IIIE)*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `(AJ37)`, *(MiG-21bis)*, J35D"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 `[Kfir Canard]`"],
            },
        ],
    },
    "10.0": {
        "title": "10.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[F-105D]`, `(AV-8C)`, F8U-2"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 `[Tornado IDS]`, `[Su-22UM3K]`, `[F-4F Early]`, `[Hunter F.58]`"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[Su-22M3]`, `[Су-25 / K]`, **Su-17M2**, *(Як-28Б)*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 *(Harrier GR.3)*, *(Harrier GR.1)*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *(F-1)*, *(Alpha Jet TH)*, *(AV-8S)*, F-104J"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 *(A-5C)*, **F-104G**"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `[Tornado IDS]`, `[Su-22M3]`, **F-104G**"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 `[Mirage 5F]`, *(Mirage IIIC)*, *(F-104G)*, F-8E(FN)"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 `[Ayit]`, Nesher, Shahak"],
            },
        ],
    },
    "9.7": {
        "title": "9.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 **AV-8C**"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 `[Hunter F.58]`, *MiG-21 SPS-K*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *(Як-28Б)*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 **Harrier GR.3**"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 `[Alpha Jet TH]`, `[AV-8S]`, T-2 / Early"],
            },
            {
                "name": "🇨🇳 China",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 *Ariete*"],
            },
            {
                "name": "🇫🇷 France",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [EMPTY_ARROW],
            },
        ],
    },
    "9.3": {
        "title": "9.3",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `A-4E Early`"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *MiG-21 SPS-K*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *Як-28Б*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 `Buccaneer S.2`"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇨🇳 China",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `IAR-93B`, *Ariete*"],
            },
            {
                "name": "🇫🇷 France",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [EMPTY_ARROW],
            },
        ],
    },
    "9.0": {
        "title": "9.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[FJ-4B VMF-232]`, `[F4D-1]`, A-4B, *(F11 F-1)*, F3H-2"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 `[G.91 R/3/4]`, *(Alpha Jet A)*, *(Me 163 B-0)*, Lim-5P"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[Yak-23]`, МиГ-17АС, Mig-17"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 `[Scimitar]`, *(Sea Vixen)*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *(Alpha Jet A)*, *(Ki-200)*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 J-4"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `[G.91 R/4]`, `[G.91Y]`, Mig-17PF"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 Etendard, *(Alpha Jet E)*, Super Mystere"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 A32A"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 `[Sa'ar]`"],
            },
        ],
    },
    "8.7": {
        "title": "8.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 A-4B"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 G.91 R/3/4, Lim-5P, Me 163 B-0"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 Yak-23, Mig-17"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 `[Scimitar]`, Buccaneer S.1, `[Sea Vixen]`"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 Ki-200"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 J-4"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 G.91 R/4, Mig-17PF"],
            },
            {
                "name": "🇫🇷 France",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `[SAAB-105OE]`, `[SAAB-105G]`"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [EMPTY_ARROW],
            },
        ],
    },
    "8.3": {
        "title": "8.3",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[F-84F]`, *F-86F-25 / 35*, *F9F-8*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 `[F-84F]`, *(MiG-15bis)*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *(МиГ-15бис ИШ)*, **Ил-28/Ш**, *(МиГ-15бис)*, *БИ*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 *(Meteor F Mk.8 Reaper)*, *Meteor F Mk.8*, *Swift F.1*, *Javelin F.(A.W.) Mk.9*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *F-86F-30*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 **H-5**, *(J-2)*, *F-86F-30*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 *G.91 pre-serie*, *CL-13 Mk.4*"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *F-84F*, *M.D.452 IIC*, *Meteor F Mk.8*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `[SAAB-105OE]`, `[SAAB-105G]`, *J29D*"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 `[F-84F]`, `[A-4H]`, *Meteor F Mk.8*"],
            },
        ],
    },
    "8.0": {
        "title": "8.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 *(F-80C-10)*, *(F9F-2)*, *(F-86A-5)*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 **Ar 234 C-3**, `[Me 262 C-1a]`, *Me 163 B*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[МиГ-15бис ИШ]`, **Ил-28/Ш**, *МиГ-15*, *БИ*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 `[Meteor F Mk.8 Reaper]`, *(Meteor F Mk.8)*, *Vampire F.B.5*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 **H-5**"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 *Vampire FB 52A*"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *(Meteor F Mk.8)*, M.D.452 IIA"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `[SK60B]`, *Vampire FB 52A*"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *(M.D.450B)*, *(Meteor F Mk.8)*"],
            },
        ],
    },
    "7.7": {
        "title": "7.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 *(F-80C-10)*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 **Ar 234 C-3**, `[Me 262 C-1a]`"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 **Ил-28/Ш**, *Ла-200*, *БИ*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 *(Meteor F Mk.4 G.41F)*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 **H-5**"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *(M.D.450B)*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 *(SK60B)*, *A29B*, *J29A*"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *(M.D.450B)*, *Meteor NF.13*"],
            },
        ],
    },
    "7.3": {
        "title": "7.3",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[F-84B-26]`, **A2D-1**, *(F2H-2)*, *(F-89B/D)*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *(Me 262 A-1a/U1 / U4)*, Ho 229 V3, `[Ar 234 C-3]`, Ju 288 C, He 177 A-5/A-3, `[Me 262 C-1a]`"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *(Су-11)*, *(Ту-2С-59)*, Ту-2С/-44, `[БИ]`, МиГ-9 (л)"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 Lincoln B Mk.II, *(Sea Meteor F Mk.3)*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *(Kikka)*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 **Tu-2S-44**, *(MiG-9 (l))*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 *(Tu-2S-59)*"],
            },
            {
                "name": "🇫🇷 France",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `[SK60B]`"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [EMPTY_ARROW],
            },
        ],
    },
    "7.0": {
        "title": "7.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[F-84B-26]`, F8F-1B, **A2D-1**, **B-29A-BN**, *(F-89B/D)*, *(F-80A-5)*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *(Ar 234 B-2)*, *(Me 262 A-1/U4)*, *(Ju 288 C)*, He 177 A-5/A-3, *(Me 262 A-1a/Jabo)*, Me 262 A-2a, Ho 229 V3"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[Ту-2С-59]`, *(Ту-2С/-44)*, `[БИ]`, *(Су-9)*, Як-15"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 Attacker FB.1/2, *(Spitfire LF Mk.IX)*, *(Spitfire F Mk.24)*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *(Kikka)*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 *(Tu-2S-44)*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `[Tu-2S-59]`"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 F8F-1B"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 `[SK60B]`, A21RB"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *(Spitfire LF Mk.IXe Вейцмана)*"],
            },
        ],
    },
    "6.7": {
        "title": "6.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 `[F8F-1B]`, A-1H, Spitfire LF Mk.IXc"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *(Me 262 A-1/U4)*, **Ar 234 B-2**, Me 262 A-2a"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 *Як-9УТ*, `[Ту-2С-59]`, *(Ту-2С/-44)*, `[БИ]`"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 Strikemaster Mk.88, *Spitfire LF Mk.IXc*, *Spitfire F Mk.24*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *N1K2-J/a*, *Ki-84 hei*, *J6K1*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 *(Tu-2S-44)*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `[Tu-2S-59]`, *G.56*"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 `[F8F-1B]`, *F4U-7*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 *A21RB*"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *Spitfire LF Mk.IXe Вейцмана*"],
            },
        ],
    },
    "6.3": {
        "title": "6.3",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 *(F8F-1B)*, A-1H, `[Spitfire LF Mk.IXc]`"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 `[Ar 234 B-2]`, `[Ju 288 C]`, He 177 A-5/A-3, He 162 A-1 / 2"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[Як-9УТ]`, `[Ту-2С-59]`, *(Ту-2С/-44)*, `[Spitfire Mk.IXc]`, Як-15П"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 Strikemaster Mk.88, Lincoln B Mk.II, `[Spitfire LF Mk.IXc]`"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *N1K2-J/a*, *Ki-84 hei*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 *(Tu-2S-44)*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `[Tu-2S-59]`, G.56"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *(F8F-1B)*, *F4U-7*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 `[Spitfire LF Mk.IXe Вейцмана]`"],
            },
        ],
    },
    "6.0": {
        "title": "6.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 **AU-1**, **F4U-4B**, `[Spitfire LF Mk.IXc]`, *(P-59A)*, *(F2G-1)*"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 `[Ju 288 C]`, He 177 A-5/A-3, *(Bf 109 K-4)*, He 162 A-1 / 2"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 `[Як-9УТ]`, `[Ту-2С-59]`, *(Ту-2С/-44)*, `[Spitfire Mk.IXc]`, Як-3У/(БК-107)"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 Lincoln B Mk.II, `[Spitfire LF Mk.IX]`, Tempest Mk.II"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 *N1K2-J/a*, *J2M3/5*"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 *(Tu-2S-44)*"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 `[Tu-2S-59]`, Re.2005 serie 0"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 *(F4U-7)*"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [EMPTY_ARROW],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 `[Spitfire LF Mk.IXe Вейцмана]`"],
            },
        ],
    },
    "5.7": {
        "title": "5.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 **F8F-1, AU-1, AM-1, F4U-4B**, *Spitfire LF Mk.IXc*, P-59A"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 *Bf 109 K-4/G-10*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 **`[Ту-2С-59]`**, **(Ту-2С/-44)**, *`[Spitfire Mk.IXc]`, Як-3У/(ВК-107)*"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 **Lancaster B Mk.III/L**, *Spitfire LF Mk.IXc*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 Ki-84 otsu, A7M2, A6M5 otsu"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 **(Tu-2S-44), Ki-84 ko**"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 **(Tu-2S-59), G.55S**"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 S.O.8000 Narval"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 —"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *Spitfire LF Mk.IXc Вейцмана*"],
            },
        ],
    },
    "5.3": {
        "title": "5.3",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 **F8F-1**"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 **Ju 188 A-2**"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 **`[Ту-2С/-44]`**"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 **Lancaster B Mk.III/L**, *Spitfire*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 A7M2, A6M5 otsu"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 **(Tu-2S-44), Ki-84 ko**"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 G.55S"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 —"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 —"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 —"],
            },
        ],
    },
    "5.0": {
        "title": "5.0",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 (**F8F-1**), (BTD-1), (SB2C-4), B-26B, XP-55, F4U-1C"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 **Me 264, Do 217 M-1 / K-1 / E-4**, *`[Bf 109 G-6]`*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 **Як-9К**, `[Ту-2]`, (Пе-8), Пе-2-359, Ер-2 (АЧ-30Б), Бе-6, Як-9П"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 Wyvern S.4, *`[Spitfire Mk.Vc]`*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 (B7A2 (Homare 23)), (SB2C-5), B7A2, `[A7M1]`, (A6M5), (J2M2/4/5)"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 —"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 G.55S"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 (SB2C-5), B-26C, M.B.162"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 T18B I (57), *`[Bf 109 G-6]`*"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *(Spitfire Mk.IXc)*"],
            },
        ],
    },
    "4.7": {
        "title": "4.7",
        "recommended": "[]",
        "decent": "()",
        "edge_case": "None",
        "trials": "{}",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": ["👉 **F8F-1**, *(SB2C-4)*, (BTD-1), B-26B, XP-55, P-63A-10/C-5"],
            },
            {
                "name": "🇩🇪 Germany",
                "items": ["👉 Do 335 A-1, Do 217 M-1 / K-1 / E-4, *`[Bf 109 G-6]`*"],
            },
            {
                "name": "🇷🇺 USSR",
                "items": ["👉 **Як-9К**, `[Ту-2]`, (Пе-8), Пе-2-359, Ер-2 (АЧ-30Б)"],
            },
            {
                "name": "🇬🇧 Britain",
                "items": ["👉 Brigand B 1, Wyvern S.4, *Spitfire*"],
            },
            {
                "name": "🇯🇵 Japan",
                "items": ["👉 (B7A2 (Homare 23)), (SB2C-5), B7A2"],
            },
            {
                "name": "🇨🇳 China",
                "items": ["👉 —"],
            },
            {
                "name": "🇮🇹 Italy",
                "items": ["👉 —"],
            },
            {
                "name": "🇫🇷 France",
                "items": ["👉 (SB2C-5), B-26C, P-63C-5"],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": ["👉 T18B I (57), *`[Bf 109 G-6]`*"],
            },
            {
                "name": "🇮🇱 Israel",
                "items": ["👉 *`[Spitfire Mk.IXc]`*"],
            },
        ],
    },

}


TANK_BR_DATA: Dict[str, BRInfo] = {
    "12.7": {
        "title": "12.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**HSTV-L**",
                    "**AGS**",
                    "**RDF/LT**",
                    "**M1A2/(Click-bait!)**",
                    "*CLAWS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Puma VJTF**",
                    "**Vilkas**",
                    "**Leopard 2A7/2A7+**",
                    "**Leopard 2A7V**",
                    "*IRIS-T SLM*",
                    "*Skynex*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-80UD**",
                    "**T-90A**",
                    "**T-90M (Proryv-3)**",
                    "**Object 292**",
                    "*Pantsir-S1*",
                    "*Strela-10M4*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Challenger 2 (2F)**",
                    "**Challenger 3 (TES)**",
                    "**Challenger 2 (TES)**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 10**",
                    "**TKX (Type 10)**",
                    "**Type 90 (B)**",
                    "*Type 87C*",
                    "*Type 81 (C)*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ99A**",
                    "**ZTZ99-III**",
                    "**ZTQ15 (VT-5)**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Ariete (PSO)**",
                    "**Centauro II 120**",
                    "**Centauro II 105/50**",
                    "*OTOMATIC*",
                    "*SIDAM 25 (Mistral)*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**Leclerc SXXI**",
                    "**Leclerc 2**",
                    "**Leclerc 1**",
                    "*SAMP/T*",
                    "*Roland 3*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 122B PLSS**",
                    "**Strv 122B+**",
                    "**Strv 122A**",
                    "*Lvkv 9040C*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.4M**",
                    "**Merkava Mk.4B**",
                    "**Merkava Mk.4 LIC**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "12.0": {
        "title": "12.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**HSTV-L**",
                    "**AGS**",
                    "**RDF/LT**",
                    "**M1A1/(Click-bait!)**",
                    "*CLAWS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Puma VJTF**",
                    "**Vilkas**",
                    "**Leopard 2A7/2A6**",
                    "**Leopard 2A6**",
                    "*IRIS-T SLM*",
                    "*Skynex*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-80UD**",
                    "**T-80BVM**",
                    "**T-90A**",
                    "**Object 292**",
                    "*Pantsir-S1*",
                    "*Strela-10M4*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Challenger 2 (TES)**",
                    "**Challenger 2**",
                    "**Challenger 2 (2F)**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 10**",
                    "**Type 90 (B)**",
                    "**Type 90 (F1)**",
                    "*Type 87C*",
                    "*Type 81 (C)*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ99A**",
                    "**ZTZ99-III**",
                    "**ZTZ96A**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Ariete AMV**",
                    "**Ariete (PSO)**",
                    "**Centauro II 120**",
                    "*OTOMATIC*",
                    "*SIDAM 25 (Mistral)*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**Leclerc SXXI**",
                    "**Leclerc 2**",
                    "**Leclerc 1**",
                    "*SAMP/T*",
                    "*Roland 3*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 122B PLSS**",
                    "**Strv 122B+**",
                    "**Strv 121**",
                    "*Lvkv 9040C*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.4M**",
                    "**Merkava Mk.4B**",
                    "**Merkava Mk.4 LIC**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "11.7": {
        "title": "11.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**M1A1 HC**",
                    "**M1A1 AIM**",
                    "**M1A2**",
                    "*M247*",
                    "*ADATS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Puma VJTF**",
                    "**Vilkas**",
                    "**Leopard 2A7/2A6**",
                    "**Leopard 2A6**",
                    "*IRIS-T SLM*",
                    "*Skynex*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-80BVM**",
                    "**T-80U**",
                    "**T-90A**",
                    "**T-72B3**",
                    "*Pantsir-S1*",
                    "*Strela-10M4*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Challenger 2**",
                    "**Challenger 2 (2F)**",
                    "**Challenger 2 (TES)**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 90**",
                    "**Type 90 (B)**",
                    "**Type 90 (F1)**",
                    "*Type 87C*",
                    "*Type 81 (C)*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ99-II**",
                    "**ZTZ99-III**",
                    "**ZTZ96A**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Ariete AMV**",
                    "**Ariete (PSO)**",
                    "**Centauro II 120**",
                    "*OTOMATIC*",
                    "*SIDAM 25 (Mistral)*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**Leclerc S2**",
                    "**Leclerc S1**",
                    "**AMX-40**",
                    "*Roland 3*",
                    "*SAMP/T*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 122A**",
                    "**Strv 121**",
                    "**Strv 122B**",
                    "*Lvkv 9040C*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.4B**",
                    "**Merkava Mk.4 LIC**",
                    "**Merkava Mk.3 Baz**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "11.3": {
        "title": "11.3",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**M1A1 HC**",
                    "**M1A1 AIM**",
                    "**M1IP**",
                    "*M247*",
                    "*ADATS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Puma VJTF**",
                    "**Vilkas**",
                    "**Leopard 2A5**",
                    "**Leopard 2A6**",
                    "*IRIS-T SLM*",
                    "*Gepard 1A2*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-80U**",
                    "**T-80B**",
                    "**T-72B3**",
                    "**T-72B (1989)**",
                    "*Pantsir-S1*",
                    "*Strela-10M4*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Challenger Mk.3**",
                    "**Challenger Mk.2**",
                    "**Challenger Mk.1**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 90**",
                    "**Type 90 (B)**",
                    "**Type 74 (F)**",
                    "*Type 81 (C)*",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ99**",
                    "**ZTZ96A**",
                    "**ZTZ96**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Centauro I 120**",
                    "**Ariete**",
                    "**Ariete (PSO)**",
                    "*OTOMATIC*",
                    "*SIDAM 25 (Mistral)*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**Leclerc S1**",
                    "**AMX-40**",
                    "**AMX-32 (120)**",
                    "*Roland 3*",
                    "*AMX-30 DCA*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 122A**",
                    "**Strv 121**",
                    "**Strv 122B**",
                    "*Lvkv 9040C*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.4 LIC**",
                    "**Merkava Mk.3 Baz**",
                    "**Merkava Mk.3D**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "11.0": {
        "title": "11.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**M1128**",
                    "**M1A1 HC**",
                    "**M1A1 AIM**",
                    "*M247*",
                    "*ADATS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Puma VJTF**",
                    "**Vilkas**",
                    "**Leopard 2A5**",
                    "**Leopard 2A4**",
                    "*IRIS-T SLM*",
                    "*Gepard 1A2*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-80B**",
                    "**T-72B (1989)**",
                    "**T-72A**",
                    "**T-55АМ-1**",
                    "*Pantsir-S1*",
                    "*Strela-10M4*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Challenger Mk.3**",
                    "**Challenger Mk.2**",
                    "**Vickers Mk.7**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 90 (B)**",
                    "**Type 90**",
                    "**Type 74 (F)**",
                    "*Type 81 (C)*",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ99**",
                    "**ZTZ96A**",
                    "**ZTQ15 (VT-5)**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Centauro I 120**",
                    "**Ariete**",
                    "**OF-40 MTCA**",
                    "*OTOMATIC*",
                    "*SIDAM 25*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**Leclerc S1**",
                    "**AMX-40**",
                    "**AMX-32 (120)**",
                    "*Roland 3*",
                    "*AMX-30 DCA*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 122A**",
                    "**Strv 121**",
                    "**Strv 122B**",
                    "*Lvkv 9040C*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.3 Baz**",
                    "**Merkava Mk.2D**",
                    "**Merkava Mk.3D**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "10.7": {
        "title": "10.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**M1128**",
                    "**120S**",
                    "**XM975**",
                    "*M163 VADS*",
                    "*ADATS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Leopard 2A4**",
                    "**KPz-70**",
                    "**TAM 2C**",
                    "*FlaRakPz 1*",
                    "*Gepard 1A2*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-80B**",
                    "**T-72B (1989)**",
                    "**T-64BV**",
                    "*2С6 Tunguska*",
                    "*Strela-10M*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Challenger Mk.3**",
                    "**Vickers Mk.7**",
                    "**Chieftain Mk.10**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 90**",
                    "**Type 74 (G)**",
                    "**Type 74 (E)**",
                    "*Type 81 (C)*",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ99**",
                    "**ZTZ96A**",
                    "**ZTZ96**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Centauro I 120**",
                    "**Centauro I (105)**",
                    "**OF-40 MTCA**",
                    "*OTOMATIC*",
                    "*SIDAM 25*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**AMX-40**",
                    "**AMX-32 (120)**",
                    "**AMX-30B2**",
                    "*Roland 3*",
                    "*AMX-30 DCA*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 121**",
                    "**Strv 101**",
                    "**Strv 102**",
                    "*Lvkv 9040C*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.3 Baz**",
                    "**Merkava Mk.2D**",
                    "**Merkava Mk.1D**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "10.3": {
        "title": "10.3",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**M1128**",
                    "**120S**",
                    "**XM975**",
                    "*M163 VADS*",
                    "*ADATS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Leopard 2K**",
                    "**KPz-70**",
                    "**TAM 2C**",
                    "*FlaRakPz 1*",
                    "*Gepard 1A2*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-72B**",
                    "**T-80B**",
                    "**T-64BV**",
                    "*2С6 Tunguska*",
                    "*Strela-10M*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Vickers Mk.7**",
                    "**Challenger Mk.3**",
                    "**Chieftain Mk.10**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 74 (G)**",
                    "**Type 74 (E)**",
                    "**Type 74 (F)**",
                    "*Type 81 (C)*",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ96A**",
                    "**ZTZ96**",
                    "**ZTQ62**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Centauro I 120**",
                    "**Centauro I (105)**",
                    "**OF-40 MTCA**",
                    "*OTOMATIC*",
                    "*SIDAM 25*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**AMX-40**",
                    "**AMX-32 (120)**",
                    "**AMX-32 (105)**",
                    "*Roland 3*",
                    "*AMX-30 DCA*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 121**",
                    "**Strv 101**",
                    "**Strv 102**",
                    "*Lvkv 9040*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.3 Baz**",
                    "**Merkava Mk.2D**",
                    "**Merkava Mk.1D**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "10.0": {
        "title": "10.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**M1128**",
                    "**120S**",
                    "**XM975**",
                    "*M163 VADS*",
                    "*ADATS*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Leopard 2K**",
                    "**KPz-70**",
                    "**TAM 2C**",
                    "*FlaRakPz 1*",
                    "*Gepard 1A2*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**T-72B**",
                    "**T-80B**",
                    "**T-64BV**",
                    "*2С6 Tunguska*",
                    "*Osa-AKM*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Chieftain Mk.10**",
                    "**Challenger Mk.2**",
                    "**Chieftain Mk.9**",
                    "*Stormer ADATS*",
                    "*Stormer HVM*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 74 (G)**",
                    "**Type 74 (E)**",
                    "**Type 74 (F)**",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ96**",
                    "**ZTZ96A**",
                    "**Type 69-IIa**",
                    "*PGZ09*",
                    "*PGZ04A*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Centauro I (105)**",
                    "**OF-40 MTCA**",
                    "**OF-40 (105)**",
                    "*OTOMATIC*",
                    "*SIDAM 25*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**AMX-40**",
                    "**AMX-32 (120)**",
                    "**AMX-32 (105)**",
                    "*AMX-30B2*",
                    "*Roland 3*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 121**",
                    "**Strv 101**",
                    "**Strv 102**",
                    "*Lvkv 9040*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.3 Baz**",
                    "**Merkava Mk.2B**",
                    "**Merkava Mk.1B**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "9.7": {
        "title": "9.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**XM1 (GM/Chrysler)**",
                    "**Merkava 2B**",
                    "**M1A1 HC**",
                    "*LAV-AD*",
                    "*M247*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Begleitpanzer 57**",
                    "**Radkampfwagen 90**",
                    "**Leopard 1A5**",
                    "*Gepard 1A2*",
                    "*Ozelot*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**БМП-2М**",
                    "**2С38**",
                    "**Т-80Б**",
                    "**Т-55АМ-1**",
                    "*Оса-АК*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Challenger Mk.2**",
                    "**Challenger Mk.3**",
                    "**Vickers Mk.7**",
                    "*Stormer ADATS*",
                    "*Rapier FSA*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 74 (G)**",
                    "**Type 74 (E)**",
                    "**Type 74 (F)**",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**ZTZ88A**",
                    "**ZTZ88C**",
                    "**PTZ89**",
                    "*PGZ09*",
                    "*Type 65*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**Centauro (ROMOR)**",
                    "**OF-40 MTCA**",
                    "**OF-40 (105)**",
                    "*OTOMATIC*",
                    "*SIDAM 25*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**AMX-30 Super**",
                    "**AMX-32 (120)**",
                    "**AMX-32 (105)**",
                    "*AMX-10P*",
                    "*Roland 3*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Strv 101**",
                    "**Strv 104**",
                    "**Strv 103C**",
                    "*Lvkv 9040*",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Merkava Mk.2D**",
                    "**Merkava Mk.2B**",
                    "**Merkava Mk.1B**",
                    "*Machbet*",
                    "*M163*",
                ],
            },
        ],
    },
    "9.3": {
        "title": "9.3",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**XM1 (GM/Chrysler)**]",
                    "**(MBT-70)**",
                    "**(Merkava 2B)**",
                    "[*M247*]",
                    "*(Imp.Chaparral)*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "[**Begleitpanzer 57**]",
                    "**(TAM 2IP)**",
                    "[**VT1-2**]",
                    "**(KPz-70)**",
                    "**(T-72M1)**",
                    "**(Leopard 1A1 (L/44))**",
                    "**(Leopard 1A5)**",
                    "*(C2A1)*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "[**БМД-4М**]",
                    "**(2С25)**",
                    "**(БМП-3)**",
                    "**(Т-72А)**",
                    "**(Т-64А)**",
                    "**(Объект 279)**",
                    "**Объект 775**",
                    "[*ЗСУ-23-4М4*]",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Rooikat MTTD)**",
                    "**(VFM5)**",
                    "**(Khalid)**",
                    "**Olifant Mk.2**",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Type 16)**",
                    "**Type 89**",
                    "**Type 87 RCV**",
                    "**(Type 74 (G/E/F))**",
                    "*(Type 93)*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**WMA301**",
                    "**PTL02**",
                    "**(ZTZ96)**",
                    "**PTZ89**",
                    "**AFT09**",
                    "[*PGZ04A*]",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "[**VCC-80/60**]",
                    "**(Centauro I 105)**",
                    "**VBC (PT2)**",
                    "**(OF-40 (MTCA))**",
                    "**(T-72M1)**",
                    "**(Leopard 1A5)**",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(VBCI)**",
                    "**(AMX-32)**",
                    "*(SANTAL)*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Ikv 91-105**",
                    "**CV9030FIN**",
                    "**(T-72M1)**",
                    "**(Leopard 1A5NO2)**",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [],
            },
        ],
    },
    "9.0": {
        "title": "9.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**XM1 (Chrysler)**]",
                    "[**XM803**]",
                    "**(Merkava Mk. 1)**",
                    "[*M247*]",
                    "*(Imp.Chaparral)*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "[**Class 3 (P)**]",
                    "**(TAM)**",
                    "[**VT1-2**]",
                    "**(Leopard 1A1)**",
                    "*Gepard*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "[**БМП-3**]",
                    "[**Объект 279**]",
                    "**(Т-62М-1)**",
                    "**T-55АМ-1/АМД-1**",
                    "**Объект 435**",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Vickers Mk.11)**",
                    "**(Rooikat Mk.1D)**",
                    "**Badger**",
                    "**(Chieftain Mk. 10)**",
                    "*ZA-35*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Type 89)**",
                    "**Type 87 RCV**",
                    "**(Type 74 E/F)**",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(WMA301)**",
                    "**(PTL02)**",
                    "**(T-69 II G)**",
                    "**PTZ89**",
                    "**AFT09**",
                    "*(PGZ09)*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**(OF-40 Mk.2A)**",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "*AMX-30 S DCA*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "[**Ikv 91-105**]",
                    "**T-55M**",
                    "*ItPsV Leopard*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Magach 6M**",
                    "**Sho't Kal Dalet**",
                ],
            },
        ],
    },
    "8.7": {
        "title": "8.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**M551**",
                    "**M3 Bradley**",
                    "**M60A1 RISE**",
                    "*(XM246)*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**JaPz.K A2**",
                    "[**VT1-2**]",
                    "**Turm III**",
                    "*Gepard*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "[**БМП-2**]",
                    "**(Объект 685)**",
                    "**(Т-62)**",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Vickers Mk.11)**",
                    "**(Rooikat Mk.1D)**",
                    "**(Chieftain Mk. 3/5)**",
                    "*ZA-35*",
                    "*Chieftain Marksman*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 74 (C)**",
                    "**STB-2**",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(Object 122МТ \"МТ\")**",
                    "**(T-62 No545)**",
                    "*(PGZ09)*",
                    "[*WZ305*]",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "*SIDAM 25*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**SK-105A2**",
                    "**AMX-10RC**",
                    "**MEPHISTO**",
                    "**AMX-30B2 BRENUS**",
                    "[*AMX-30 S DCA*]",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**BMP-2MD**",
                    "**Strv 104**",
                    "[*ItPsV Leopard*]",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Tiran 6**",
                    "**Sho't Kal Gimel**",
                    "**Magach 6 B/R Hydra**",
                ],
            },
        ],
    },
    "8.3": {
        "title": "8.3",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**(M3 Bradley)**",
                    "**(XM800T)**",
                    "**M60A1 AOS**",
                    "*(XM246)*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "[**Turm III**]",
                    "**M48A2 G A2**",
                    "*Gepard*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "[**T-55A**]",
                    "**(Объект 140)**",
                    "**(Т-10М)**",
                    "**ИС-7**",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "[**Warrior**]",
                    "**(Vickers Mk.3)**",
                    "**(Vijayanta)**",
                    "**(Olifant Mk.1A)**",
                    "*ZA-35*",
                    "*Chieftain Marksman*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "[**Type 74 (C)**]",
                    "[**STB-2**]",
                    "*Type 87*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(M41D)**",
                    "**(ZTZ59D1)**",
                    "**(Type 69-IIa)**",
                    "[*WZ305*]",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "*SIDAM 25*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "[**AMX-10RC**]",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Vidar**",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [],
            },
        ],
    },
    "8.0": {
        "title": "8.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**M551**]",
                    "**M60**",
                    "**T54E1**",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Leopard 1**",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "[**TO-55**]",
                    "**(Объект 906)**",
                    "**(Т-10А)**",
                    "**(Т-54 (49)/(51))**",
                    "**Объект 120**",
                    "*(ЗСУ-37-2)*",
                    "*(ЗСУ-23-4)*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "[**Vickers Mk.1**]",
                    "**(Centurion Mk.10)**",
                    "**(Fox)**",
                    "**Conqueror**",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(M41D)**",
                    "**(Type 69)**",
                    "**(ZTZ59A)**",
                    "**(Type 59)**",
                    "[*WZ305*]",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**OF-40**",
                    "**AUBL/74 HVG**",
                    "**M60A1**",
                    "**R3 T106 FA**",
                    "*ZSU-23-4*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**AMX-30 (1972)**",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**(Strv 101)**",
                    "**(T-54)**",
                    "**(Vidar)**",
                    "**Strv 103A**",
                    "**U-SH 405**",
                    "*VEAK 40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [],
            },
        ],
    },
    "7.7": {
        "title": "7.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**(M103)**",
                    "**T54E2**",
                    "**T114**",
                    "**M48A1**",
                    "*M163*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**(Maus/E-100)**",
                    "**M48A2 C**",
                    "**PzH 2000**",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "[**T-10A**]",
                    "**(ИС-6)**",
                    "**(ИС-4М)**",
                    "**T-54 (1947)**",
                    "[*ЗСУ-37-2*]",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "[**Conqueror**]",
                    "[**Caernarvon**]",
                    "[**Centurion Mk.3/5/1/Action X**]",
                    "*Scimitar*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Ho-Ri Production**",
                    "*Type 99*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**PLZ05**",
                    "**M48A1**",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "[**FIAT 6614 FIROS**]",
                    "**M47 (105/55)**",
                    "**PzH 2000HU**",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(Lorraine 40t)**",
                    "**(Somua SM)**",
                    "**AMX-50 Surbaissé/Surblindé**",
                    "**E.B.R. (1963)**",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "[**Strv 81/(RB 52)**]",
                    "[*VEAK 40*]",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Sho't**",
                    "**Magach 1/2**",
                    "*Hovet*",
                ],
            },
        ],
    },
    "7.3": {
        "title": "7.3",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**T32**]",
                    "**(T29/30)**",
                    "**(M551(76))**",
                    "**M47**",
                    "[*M163*]",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**Tiger II (10,5 cm)/Sla. 16/(H)/(P)**",
                    "**Ru 251**",
                    "**mKPz M47 G**",
                    "*Kugelblitz/Coelian*",
                    "*Wiesel 1A4*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(ИС-3)**",
                    "**(Т-44-100)**",
                    "**Объект 268**",
                    "**2С19М2**",
                    "[*ЗСУ-23-4М2*]",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "[**FV4202**]",
                    "**(Centurion Mk.2)**",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Ho-Ri Production)**",
                    "**M47**",
                    "*Type 99*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**PLZ83-130**",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**FIAT 6614**",
                    "**R3 T20 FA-HS**",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**AuF1**",
                    "**AMX-50 Foch**",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**Kungstiger**",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Sholef**",
                    "[*Hovet*]",
                ],
            },
        ],
    },
    "7.0": {
        "title": "7.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**M551(76)**]",
                    "**(T29/30/34)**",
                    "**M6A2E1**",
                    "**T26E1-1/E5**",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "[**Tiger II (10,5 cm)/Sla. 16/(H)**]",
                    "**(Tiger II (P))**",
                    "*Kugelblitz/Coelian*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(T-44-100)**",
                    "**(ИС-2 (1944))**",
                    "**Объект 268**",
                    "**2С19М1**",
                    "*(M53/59)*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "[**Centurion Mk.2**]",
                    "**G6**",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Ho-Ri Prototype)**",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(IS-2 (1944))**",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**FIAT 6614**",
                    "**C13 T90**",
                    "*(R3 T20 FA-HS)*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**AuF1**",
                    "**AMX M4**",
                    "**E.B.R (1954)**",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "[**Kungstiger**]",
                    "**Bkan 1C**",
                    "**Pbv 501**",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [],
            },
        ],
    },
    "6.7": {
        "title": "6.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**(T34)**",
                    "**(M6A2E1)**",
                    "**(T30)**",
                    "**T26E1-1/E5**",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "[**Tiger II Sla. 16/(H)**]",
                    "**(Tiger II (P))**",
                    "**Jagdtiger**",
                    "[*Coelian*]",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(Об. 248)**",
                    "**(ИС-2 (1944))**",
                    "**СУ-122-54**",
                    "**Type 62**",
                    "**Т-44**",
                    "*(M53/59)*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "[**Centurion Mk.2**]",
                    "**G6**",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "[**Ho-Ri Prototype**]",
                    "**ST-A3**",
                    "**Type 61**",
                    "**Type 60 SPRG**",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(IS-2 (1944))**",
                    "**Type 62**",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**FIAT 6614**",
                    "*(R3 T20 FA-HS)*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "[**Kungstiger**]",
                    "**Bkan 1C**",
                    "**Pbv 501**",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [],
            },
        ],
    },
    "6.3": {
        "title": "6.3",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**M4A3E2 (76) W**]",
                    "**(T20)**",
                    "**Super Hellcat**",
                    "**T25**",
                    "**M109A1**",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**(Jagdpanther)**",
                    "**(Tiger E)**",
                    "**(Panther A/G/Ersatz M10)**",
                    "[*Coelian*]",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "[**T-34-100**]",
                    "**(ИС-2)**",
                    "**(КВ-220)**",
                    "**(Т-V)**",
                    "**(M4A2)**",
                    "**T-44-122**",
                    "**2С3М**",
                    "*(M53/59)*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**Ratel 90**",
                    "**M109A1**",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**Type 75 SPH**",
                    "**ST-A1/A2**",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(IS-2)**",
                    "**PLZ83**",
                    "*ZSL92*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "*(R3 T20 FA-HS)*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(Panther Dauphine)**",
                    "**AMX-10P**",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**Rochev**",
                    "**M-51(W)**",
                ],
            },
        ],
    },
    "6.0": {
        "title": "6.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**(M18 GMC)**",
                    "**(M4A2 (76))**",
                    "**(M4A3E2, T1E1 (90))**",
                    "*Skink*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**(Tiger I)**",
                    "**(Panther A/G/Ersatz M10)**",
                    "*Ostwind I/Ost*",
                    "*Zerstörer 45*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(ИС-2)**",
                    "**(Т-34-85 (Д-5Т))**",
                    "**(КВ-122)**",
                    "**(ИСУ-122)**",
                    "*ЗСУ-37*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Centurion Mk.1)**",
                    "**(Challenger)**",
                    "**(Avenger)**",
                    "*Skink*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(M4A3 (76) W)**",
                    "**(Type 61)**",
                    "**(M41A1)**",
                    "*M19A1*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(IS-2)**",
                    "**(Type 62)**",
                    "**(Т-34-85 (ЗиС-С-53))**",
                    "*ZSD63*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**(M26A1)**",
                    "**(M36B1)**",
                    "**(M4 Tipo Ic)**",
                    "*R3 T20 FA-HS*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(ARL 44)**",
                    "**(AMX M4)**",
                    "*AMX-13 DCA 40*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**(Strv 81 (RB 52))**",
                    "**(Strv 81)**",
                    "*Lvkv 42*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**(M-51(W))**",
                    "**(Sho't Kal Alef)**",
                    "*M15A1 AA*",
                ],
            },
        ],
    },
    "5.7": {
        "title": "5.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**M4A2 (76)**]",
                    "[**M4A3E2**]",
                    "**M6A1**",
                    "**(T26E1-1)**",
                    "*Skink*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**(Pz.Bef.Wg. IV F1)**",
                    "**(Tiger Ost/W / Het)**",
                    "**(Panther D/A/F)**",
                    "*Ostwind I/Ost*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(КВ-1С (ЗиС-5))**",
                    "**(ИС-2)**",
                    "**(ИСУ-122)**",
                    "**(СУ-152)**",
                    "*ЗСУ-37*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Comet I)**",
                    "**(Challenger)**",
                    "**(Sherman Firefly IC)**",
                    "*Skink*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Chi-Ri II)**",
                    "**(Chi-To Late)**",
                    "**(M4A3 (76) W)**",
                    "*M19A1*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(IS-2)**",
                    "**(Type 62)**",
                    "**(T-34-85 (ЗиС-С-53))**",
                    "*ZSD63*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**(M24 (SAGM))**",
                    "**(M18 (SAGM))**",
                    "**(M4 Tipo Ic)**",
                    "*R3 T20 FA-HS*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(ARL 44)**",
                    "**(ARL 44 ACL-1)**",
                    "*AMX-13 DCA 40*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**(Strv 81 (RB 52))**",
                    "**(Strv 74)**",
                    "**(Ikv 103)**",
                    "*Lvkv 42*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**(M-51(W))**",
                    "**(M-51)**",
                    "*M15A1 AA*",
                ],
            },
        ],
    },
    "5.3": {
        "title": "5.3",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "[**M4A2 (76)**]",
                    "**(T1E1/M6A1)**",
                    "**M18 GMC**",
                    "**(M36 GMC)**",
                    "*Skink*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**(VK 45.01 (P))**",
                    "**(Panther D)**",
                    "**(Panther A)**",
                    "*Ostwind I*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(ИС-1)**",
                    "**(Т-34-85 (Д-5Т))**",
                    "**(СУ-122П)**",
                    "**(СУ-152)**",
                    "*ЗСУ-37*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Comet I)**",
                    "**(Challenger)**",
                    "**(Sherman Firefly IC)**",
                    "*Skink*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Chi-Ri II)**",
                    "**(Chi-To Late)**",
                    "**(Ho-Ni III)**",
                    "*M19A1*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(IS-2)**",
                    "**(T-34-85 (ЗиС-С-53))**",
                    "**(SU-122-54)**",
                    "*ZSD63*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**(Sherman Tipo Vc)**",
                    "**(M18 (SAGM))**",
                    "**(Breda 501)**",
                    "*R3 T20 FA-HS*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(ARL 44)**",
                    "**(ARL 44 ACL-1)**",
                    "*AMX-13 DCA 40*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**(Strv m/42 EH)**",
                    "**(Ikv 103)**",
                    "**(Ikv 91)**",
                    "*Lvkv 42*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**(M-51(W))**",
                    "**(M-50)**",
                    "*M15A1 AA*",
                ],
            },
        ],
    },
    "5.0": {
        "title": "5.0",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**(M4A1 (76) W)**",
                    "**(M41A1)**",
                    "**(T34)**",
                    "**T55E1**",
                    "**(M4A3 (105))**",
                    "*M19A1*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**(Pz.Bef.Wg. IV J)**",
                    "**(Sd.Kfz.234/3)**",
                    "**(Brummbär)**",
                    "**(Jagdpanzer IV L/70)**",
                    "*Wirbelwind*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(КВ-1С (ЗиС-5))**",
                    "**(ИС-1)**",
                    "**(ИСУ-122)**",
                    "**(ИСУ-152)**",
                    "*ЗСУ-37*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Sherman Firefly IC)**",
                    "**(Achilles)**",
                    "**(Avenger)**",
                    "**(Concept 3)**",
                    "*Skink*",
                    "*Crusader AA Mk. II*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Chi-To Late)**",
                    "**(Na-To)**",
                    "**(Type 5 Ho-Ru)**",
                    "*M19A1*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(Type 58)**",
                    "**(ИСУ-122)**",
                    "**(SU-152)**",
                    "*PGZ 34*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**(Sherman Tipo Ic)**",
                    "**(M18 (SAGM))**",
                    "**(Breda 501)**",
                    "*R3 T20 FA-HS*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(ARL 44)**",
                    "**(ARL 44 ACL-1)**",
                    "**(ARL 44 (ACL-1) Bis)**",
                    "*AMX-13 DCA 40*",
                    "*Lorraine 155*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**(Strv m/42 EH)**",
                    "**(Ikv 73)**",
                    "**(Ikv 102)**",
                    "*Lvtdgb m/40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**(Sherman M-51)**",
                    "**(Sherman M-50)**",
                    "*TCM 20*",
                ],
            },
        ],
    },
    "4.7": {
        "title": "4.7",
        "recommended": "[]",
        "decent": "[]",
        "edge_case": "None",
        "trials": "[]",
        "nations": [
            {
                "name": "🇺🇸 USA",
                "items": [
                    "**(T14)**",
                    "**(T55E1)**",
                    "**(M24)**",
                    "**(M4A3 (105))**",
                    "*M19A1*",
                ],
            },
            {
                "name": "🇩🇪 Germany",
                "items": [
                    "**(Sd.Kfz.234/4)**",
                    "**(Brummbär)**",
                    "**(Jagdpanzer IV/38(t))**",
                    "*Wirbelwind*",
                    "*Ostwind*",
                ],
            },
            {
                "name": "🇷🇺 USSR",
                "items": [
                    "**(КВ-1 (ЗиС-5))**",
                    "**(ИСУ-152)**",
                    "**(ИСУ-122)**",
                    "**(СУ-152)**",
                    "*ЗСУ-37*",
                ],
            },
            {
                "name": "🇬🇧 Britain",
                "items": [
                    "**(Sherman Firefly IC)**",
                    "**(Achilles)**",
                    "**(Avenger)**",
                    "**(Concept 3)**",
                    "*Skink*",
                    "*Crusader AA Mk. II*",
                ],
            },
            {
                "name": "🇯🇵 Japan",
                "items": [
                    "**(Sherman Tipo Ic)**",
                    "**(Chi-To Late)**",
                    "**(Na-To)**",
                    "*So-Ki*",
                ],
            },
            {
                "name": "🇨🇳 China",
                "items": [
                    "**(Type 58)**",
                    "**(ИСУ-122)**",
                    "**(SU-152)**",
                    "*PGZ 34*",
                ],
            },
            {
                "name": "🇮🇹 Italy",
                "items": [
                    "**(Sherman Tipo Ic)**",
                    "**(M18 (SAGM))**",
                    "**(Breda 501)**",
                    "*R3 T20 FA-HS*",
                ],
            },
            {
                "name": "🇫🇷 France",
                "items": [
                    "**(Lorraine 155 Mle 50)**",
                    "**(ARL 44)**",
                    "**(ARL 44 ACL-1)**",
                    "*AMX-13 DCA 40*",
                ],
            },
            {
                "name": "🇸🇪 Sweden",
                "items": [
                    "**(Strv m/42 EH)**",
                    "**(Ikv 73)**",
                    "**(Ikv 102)**",
                    "*Lvtdgb m/40*",
                ],
            },
            {
                "name": "🇮🇱 Israel",
                "items": [
                    "**(Sherman M-50)**",
                    "*TCM 20*",
                ],
            },
        ],
    },
}

class NationEquipment(TypedDict):
    name: str
    items: List[str]


class BRInfo(TypedDict):
    title: str
    recommended: str
    decent: str
    edge_case: str
    trials: str
    nations: List[NationEquipment]


class CategoryInfo(TypedDict, total=False):
    title: str
    display_name: str
    description: str
    color: discord.Color
    default_br: str
    br_buttons: Tuple[Tuple[str, discord.ButtonStyle, int], ...]
    br_data: Dict[str, BRInfo]
    notes: Tuple[str, ...]


CATEGORY_CONFIG: Dict[str, CategoryInfo] = {
    "tanks": {
        "title": "Танки 🚜",
        "display_name": "Танки",
        "color": discord.Color(0x3BA55D),
        "default_br": "12.7",
        "br_buttons": (
            ("12.7", discord.ButtonStyle.success, 0),
            ("12.0", discord.ButtonStyle.success, 0),
            ("11.7", discord.ButtonStyle.primary, 0),
            ("11.3", discord.ButtonStyle.primary, 0),
            ("11.0", discord.ButtonStyle.primary, 0),
            ("10.7", discord.ButtonStyle.secondary, 1),
            ("10.3", discord.ButtonStyle.secondary, 1),
            ("10.0", discord.ButtonStyle.secondary, 1),
            ("9.7", discord.ButtonStyle.secondary, 1),
            ("9.3", discord.ButtonStyle.secondary, 1),
            ("9.0", discord.ButtonStyle.secondary, 2),
            ("8.7", discord.ButtonStyle.secondary, 2),
            ("8.3", discord.ButtonStyle.secondary, 2),
            ("8.0", discord.ButtonStyle.secondary, 2),
            ("7.7", discord.ButtonStyle.secondary, 2),
            ("7.3", discord.ButtonStyle.secondary, 3),
            ("7.0", discord.ButtonStyle.secondary, 3),
            ("6.7", discord.ButtonStyle.secondary, 3),
            ("6.3", discord.ButtonStyle.secondary, 3),
            ("6.0", discord.ButtonStyle.secondary, 3),
            ("5.7", discord.ButtonStyle.secondary, 4),
            ("5.3", discord.ButtonStyle.secondary, 4),
            ("5.0", discord.ButtonStyle.secondary, 4),
            ("4.7", discord.ButtonStyle.secondary, 4),
        ),
        "br_data": TANK_BR_DATA,
        "notes": GROUND_NOTES,
    },
    "air": {
        "title": "Авиация ✈️",
        "display_name": "Авиация",
        "color": discord.Color(0x5865F2),
        "default_br": "12.7",
        "br_buttons": (
            ("12.7", discord.ButtonStyle.success, 0),
            ("12.0", discord.ButtonStyle.success, 0),
            ("11.7", discord.ButtonStyle.primary, 0),
            ("11.3", discord.ButtonStyle.primary, 1),
            ("11.0", discord.ButtonStyle.primary, 1),
            ("10.7", discord.ButtonStyle.secondary, 1),
            ("10.3", discord.ButtonStyle.secondary, 2),
            ("10.0", discord.ButtonStyle.secondary, 2),
            ("9.7", discord.ButtonStyle.secondary, 2),
            ("9.3", discord.ButtonStyle.secondary, 3),
            ("9.0", discord.ButtonStyle.secondary, 3),
            ("8.7", discord.ButtonStyle.secondary, 3),
            ("8.3", discord.ButtonStyle.secondary, 4),
            ("8.0", discord.ButtonStyle.secondary, 4),
            ("7.7", discord.ButtonStyle.secondary, 4),
            ("7.3", discord.ButtonStyle.secondary, 5),
            ("7.0", discord.ButtonStyle.secondary, 5),
            ("6.7", discord.ButtonStyle.secondary, 5),
            ("6.3", discord.ButtonStyle.secondary, 6),
            ("6.0", discord.ButtonStyle.secondary, 6),
            ("5.7", discord.ButtonStyle.secondary, 7),
            ("5.3", discord.ButtonStyle.secondary, 7),
            ("5.0", discord.ButtonStyle.secondary, 7),
            ("4.7", discord.ButtonStyle.secondary, 7),
        ),
        "br_data": AIR_BR_DATA,
        "notes": AIR_NOTES,
    },
}

def build_initial_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Выберите тип техники",
        description=(
            "Нажмите на нужную кнопку, чтобы увидеть мету по технике.\n\n"
            f"```{BR_SCHEDULE}```"
        ),
        color=MAIN_EMBED_COLOR,
    )
    embed.set_footer(text=FOOTER_TEXT)
    return embed


def build_category_embed(category_key: str) -> discord.Embed:
    config = CATEGORY_CONFIG[category_key]
    embed = discord.Embed(
        title=str(config["title"]),
        description=str(config.get("description", "")),
        color=config.get("color", MAIN_EMBED_COLOR),
    )
    embed.set_footer(text=FOOTER_TEXT)
    return embed


GROUND_NOTES: Tuple[str, ...] = (
    "Ground:",
    "Рамка -> Дрон",
    "Жирный -> Танки",
    "Курсив -> ПВО",
)

AIR_NOTES: Tuple[str, ...] = (
    "Aviation:",
    "Смесь - `Универсал`",
    "Рамка - `ППВО`",
    "Жирный - Штурмовик",
    "Курсив - Истребитель",
)


def build_br_embed(category_key: str, br_label: str) -> discord.Embed:
    config = CATEGORY_CONFIG[category_key]
    br_data = config.get("br_data")
    if not br_data:
        return build_category_embed(category_key)

    try:
        info = br_data[br_label]
    except KeyError as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"BR {br_label} not configured for {category_key}") from exc

    notes = config.get("notes", GROUND_NOTES)

    lines = [
        f"Рекомендовано - {info['recommended']}",
        f"Неплохо - {info['decent']}",
        f"Крайний случай - {info['edge_case']}",
        f"Испытания - {info['trials']}",
        "",
        *notes,
    ]

    embed = discord.Embed(
        title=str(info["title"]),
        description="\n".join(lines),
        color=config.get("color", MAIN_EMBED_COLOR),
    )

    for nation in info["nations"]:
        value = ", ".join(nation["items"]) if nation["items"] else "—"
        embed.add_field(name=nation["name"], value=value, inline=False)

    embed.set_footer(text=FOOTER_TEXT)
    return embed


class EquipmentChoiceButton(discord.ui.Button["EquipmentSelectionView"]):
    """Кнопка выбора категории техники."""

    def __init__(
        self,
        *,
        label: str,
        style: discord.ButtonStyle,
        category_key: str,
        emoji: Optional[str] = None,
        custom_id: Optional[str] = None,
    ) -> None:
        super().__init__(label=label, style=style, emoji=emoji, custom_id=custom_id)
        self.category_key = category_key

    async def callback(self, interaction: discord.Interaction) -> None:  # type: ignore[override]
        config = CATEGORY_CONFIG[self.category_key]
        view = CategoryView(self.category_key)
        if config.get("br_data"):
            embed = view.get_current_embed()
        else:
            embed = build_category_embed(self.category_key)
        await interaction.response.edit_message(embed=embed, view=view)


class EquipmentSelectionView(discord.ui.View):
    """Начальный набор кнопок (танки/авиация)."""

    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(
            EquipmentChoiceButton(
                label="Танки",
                emoji="🚜",
                style=discord.ButtonStyle.success,
                category_key="tanks",
                custom_id="equipment_select_tanks",
            )
        )
        self.add_item(
            EquipmentChoiceButton(
                label="Авиация",
                emoji="✈️",
                style=discord.ButtonStyle.primary,
                category_key="air",
                custom_id="equipment_select_air",
            )
        )


class BRSelectionButton(discord.ui.Button["CategoryView"]):
    """Кнопка выбора конкретного БР."""

    def __init__(
        self,
        *,
        label: str,
        style: discord.ButtonStyle,
        row: int,
        custom_id: Optional[str] = None,
    ) -> None:
        super().__init__(label=label, style=style, row=row, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction) -> None:  # type: ignore[override]
        assert isinstance(self.view, CategoryView)
        await self.view.update_selection(interaction, self.label)


class BackButton(discord.ui.Button["CategoryView"]):
    """Возврат в главное меню выбора техники."""

    def __init__(self) -> None:
        super().__init__(
            label="Назад",
            style=discord.ButtonStyle.danger,
            row=4,
            custom_id="equipment_back",
        )

    async def callback(self, interaction: discord.Interaction) -> None:  # type: ignore[override]
        embed = build_initial_embed()
        view = EquipmentSelectionView()
        await interaction.response.edit_message(embed=embed, view=view)


class CategoryView(discord.ui.View):
    """Набор кнопок БР для выбранной категории."""

    def __init__(self, category_key: str, initial_br: Optional[str] = None) -> None:
        super().__init__(timeout=None)
        self.category_key = category_key
        self.category_info = CATEGORY_CONFIG[category_key]

        self._br_buttons = self.category_info.get("br_buttons", ())
        self._br_data = self.category_info.get("br_data")
        self.current_br = initial_br or self.category_info.get("default_br")
        if self.current_br is None and self._br_buttons:
            self.current_br = self._br_buttons[0][0]

        for label, style, row in self._br_buttons:
            sanitized_label = label.replace(".", "_")
            custom_id = f"equipment_{category_key}_br_{sanitized_label}"
            self.add_item(
                BRSelectionButton(
                    label=label,
                    style=style,
                    row=row,
                    custom_id=custom_id,
                )
            )

        self.add_item(BackButton())
        self.update_button_states()

    def has_br_data(self) -> bool:
        return bool(self._br_data)

    def get_current_embed(self) -> discord.Embed:
        if self.has_br_data() and self.current_br:
            return build_br_embed(self.category_key, str(self.current_br))
        return build_category_embed(self.category_key)

    def update_button_states(self) -> None:
        for item in self.children:
            if isinstance(item, BRSelectionButton):
                item.disabled = self.has_br_data() and item.label == str(self.current_br)

    async def update_selection(
        self, interaction: discord.Interaction, br_label: str
    ) -> None:
        if not self.has_br_data():
            await interaction.response.defer()  # pragma: no cover - no BR data branch
            return

        self.current_br = br_label
        self.update_button_states()
        embed = self.get_current_embed()
        await interaction.response.edit_message(embed=embed, view=self)


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready() -> None:  # type: ignore[override]
        logging.info("Logged in as %s (ID: %s)", bot.user, bot.user and bot.user.id)
        try:
            synced = await bot.tree.sync()
        except discord.HTTPException as exc:  # pragma: no cover - network error only
            logging.exception("Не удалось синхронизировать команды: %s", exc)
        else:
            logging.info("Синхронизировано %s команд", len(synced))

    @bot.tree.command(name="help", description="Подсказка по использованию бота")
    async def help_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message(HELP_MESSAGE, ephemeral=True)

    @bot.tree.command(name="br", description="Показать расписание БР")
    async def br_command(interaction: discord.Interaction) -> None:
        embed = build_initial_embed()
        view = EquipmentSelectionView()
        await interaction.response.send_message(embed=embed, view=view)

    return bot


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s")
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError(
            "Переменная окружения DISCORD_TOKEN не найдена. "
            "Укажите токен бота перед запуском."
        )

    bot = create_bot()
    bot.run(token)


if __name__ == "__main__":
    main()
