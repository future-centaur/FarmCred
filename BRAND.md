# STAFF

**Given to:** Farmcred. The product keeps its name. Staff decides the styling and the way a reading is spoken.
**Declared:** 2026-11-10

Staff is a gage, not a picture of a farm. A USGS Style A staff gage is a porcelain-enamel iron board, 4 inches wide, with black figures on white. Marks sit at the foot, the tenth, and the hundredth so two close readings stay separate. It is read outdoors, at a distance, on a wall or a pier.

https://www.usgs.gov/media/images/a-staff-gage-gives-a-quick-estimate-gage-height-stage-a-river
https://www.stevenswater.com/resources/datasheets/staff_gages_web.pdf

The place that proves the brand is Masinga, the reservoir at the head of the Seven Forks cascade on the Tana. KenGen and TARDA publish three facts about the same water, and they do not add them up.

| At Masinga | What it is | On a Farmcred file |
|---|---|---|
| Reservoir level, against full supply 1,056.50 m and minimum operating level 1,037 m | What the dam can hold | Yield, in kg or bags |
| Discharge through the two 20 MW turbines | What became electricity | Realized revenue, in KES |
| Overflow at the chute spillway | Water that was real and earned nothing | The gap between volume and cash |

On 2 May 2024 the reservoir stood at 1,058.22 m, above full supply, and the overflow was reported on its own while the dam was reported sound. On 21 January 2026 it stood at 1,053.04 m, 3.04 m below full supply and above the minimum operating level. A level inside the scale is still a level. High water and low water change how the reservoir is run. They are printed as the top and bottom of the scale.

https://www.kengen.co.ke/update-on-overflow-at-masinga-dam-as-at-02-05-2024/
https://www.kengen.co.ke/high-grand-falls-hydropower-project-gains-momentum-as-energy-cs-tours-the-700mw-site/
https://tarda.go.ke/masinga-dam-reservoir/

## Mark

A vertical board in the proportion of a Style A gage. Three horizontal ticks of equal weight, stacked, with air between them. Under the ticks, one heavier line: the reading. The word Farmcred sits to the right of that line, in the same black, aligned to it. No maize, no leaf, no drop of water drawn as an icon.

## Color

Taken from the gage and from the embankment, which is locally won earth and rock.

| Role | Hex | Where it sits |
|---|---|---|
| Porcelain | `#F6F4EF` | The board. Page ground, and the revenue column. |
| Enamel black | `#1C1C1C` | Figures, the limit, and Next. The same ink whether the figure is small or large. |
| Soil | `#4A463E` | Labels. The embankment, not a second brand color. |
| Dry shade | `#E3DDD0` | Ground of the second reading, so the two columns do not merge. |
| Wet concrete | `#D3DDD6` | Ground of the gap. Overflow. A cool stain beside the warm board. |
| Held water | `#1E3330` | Ground of the yield column only. Porcelain figures on it. This is the ceiling. |
| Closed gate | `#B3261E` | A hard gate, and nothing else. |

## Type

Roboto, because that is what the capture tool already uses on a cheap Android phone. Readings are weight 500, tabular figures, at the top of the scale (32 and 40). The unit is printed with the figure, the way metres are printed on the gage. Labels stay at 18.

## Voice

Say the reading and the unit. "18 bags an acre. KES 42,000 received. The gap is on the file." A missing figure is a blank graduation. It is left empty. Full supply and the minimum operating level are the ends of the scale: they size what can be held, and a reading between them is shown.

## Where a reading is written

`DESIGN_REFERENCE.md` holds the choice. A ticket writes yield and revenue when one exists. An empty mark on the board is filled when the ticket is missing. The Collect form is the ordered walk for identity, the plot pin, tenure, the crop, and one specific consent. The gap and the limit are read off the board.

## How a step moves

Water at Masinga moves one way. It is held, then it passes through the turbines. The overflow is what you see once both of those have been passed.

The step follows that path. On the board it runs from the yield mark to the revenue mark. On the form it is the Next button, and Back walks upstream. Collect's navigation is Forward and back buttons. A sideways swipe is off, and answering does not carry the form forward.

https://docs.getodk.org/collect-settings/

Next on a closed gate stays put. Area and crop are those gates. A climate reading lets the step happen. An empty yield or an empty revenue lets the step happen, and that mark stays blank.

Where the screen is drawn, Next carries the current mark up and brings the next mark up from below. Back brings the upstream mark down from above.
