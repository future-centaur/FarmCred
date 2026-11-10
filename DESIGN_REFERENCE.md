# DESIGN REFERENCE — Farmcred

**Declared:** 2026-11-10. Revised the same day from the Staff brand in `BRAND.md`, and again for how a reading is collected.
**Brand:** Staff. Farmcred keeps its name. These tokens are the brand applied to the file.

The people who touch this file are a field agent sitting with a farmer, the farmer on a narrow Android screen, and a lender reading the same facts at a desk. The board they share is a USGS Style A staff gage: porcelain enamel, black figures, marks fine enough that two close readings stay separate.

https://www.usgs.gov/media/images/a-staff-gage-gives-a-quick-estimate-gage-height-stage-a-river
https://docs.getodk.org/collect-filling-forms/
https://docs.getodk.org/collect-settings/

Yield, realized revenue, and the gap between them are three readings. Kilograms or bags, and shillings, are the largest type. The limit is the heavy line under the three. A smaller limit uses the same ink as a larger one. Red is a closed gate.

Phone type is still open (C6). DigiFarm's farmer channel is USSD (`*283#`), and this reference does not adopt that. A later feature-phone path keeps these words and this order in a shorter sequence.

```yaml
reference: https://www.usgs.gov/media/images/a-staff-gage-gives-a-quick-estimate-gage-height-stage-a-river
interaction: https://docs.getodk.org/collect-filling-forms/
navigation: https://docs.getodk.org/collect-settings/
ticket: a buying-centre slip, a milk-cooler ticket, or a weighbridge ticket — weight on one line, money on the next
brand: BRAND.md
type_scale: 18/20/24/32/40
spacing_unit: 8px rhythm, 16px screen margin, 48px minimum target
typeface: Roboto. Readings at weight 500 with tabular figures. Labels at 18.
color_roles:
  primary: "#1C1C1C"       # Enamel black. Next, every reading, and the limit.
  secondary: "#4A463E"     # Embankment soil. Labels.
  surface: "#F6F4EF"       # Porcelain. Page ground and the revenue column.
  muted: "#E3DDD0"         # Dry shade. Ground of the second reading.
  spill: "#D3DDD6"         # Wet concrete. Ground of the gap. Never a hard gate.
  reservoir: "#1E3330"     # Held water. Ground of the yield column only. Figures on it are porcelain, #F6F4EF.
  destructive: "#B3261E"   # Closed gate. Hard gates only.
component_source: The board is the staff gage, three bands and one heavy line. A ticket writes yield and revenue when one exists. ODK Collect, navigation set to Forward and back buttons, is the ordered walk for the facts only a person on the plot can supply. Material 3 components, restyled to these roles.
```

## Where a reading is written

1. A record that already exists writes the figure. Satellite crop stress, ward rainfall, county yield, a cooperative delivery book, and a mobile-money statement each write their own fact. The gap and the limit are read off the board. None of these is typed again.
2. Yield and realized revenue prefer a ticket: a buying-centre slip, a milk-cooler ticket, or a weighbridge ticket. The weight is one line. The money is the next line. The file keeps both lines.
3. When that ticket is missing, the board is the place the two figures are written. The file is already open. Tap the blank yield mark, write the figure and the unit, step downstream, and write the shillings on the revenue mark. The gap shows once both marks have been passed. It has no field of its own.
4. The Collect form is the walk an agent takes through the facts only a person on the plot can supply, in order: identity, the plot pin, tenure, the crop, and one specific yes for one use. Yield and revenue join that walk only when there is no ticket and the marks are being filled from the walk rather than from the open board.

## How a step moves

The step is downstream. Back walks upstream, to the stop just left. Moving backwards stays available.

On the board, the downstream step is from the yield mark to the revenue mark. On the form, the step is the Next button and the Back button. Collect's navigation for this project is Forward and back buttons. A sideways swipe is off. Answering does not carry the form forward by itself.

Next on a closed gate stays put. Area and crop are those gates. A climate reading lets the step happen. An empty yield or an empty revenue lets the step happen, and that mark stays blank.

Where the screen is drawn, Next carries the current mark upward and brings the next mark up from below. Back brings the upstream mark down from above.

## Shape

1. The open board shows three bands: yield on held water, realized revenue on porcelain, the gap on wet concrete. The limit sits under them as one heavy line. The three stay separate. A missing figure is a blank mark. Tapping a blank mark is how a missing ticket gets written.
2. The Collect walk is one question on a screen, porcelain ground, enamel-black figure, Next and Back fixed along the bottom. The label carries the unit.
3. The desk page uses the same type scale and colors, on a wider screen. It is the same three bands, not a dashboard of cards.
