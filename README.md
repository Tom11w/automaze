##  Shapes, mirrored and backwards.
- `'` (Prime) = **Mirror** (Swap all Ls to Rs and vice versa).
- `*` (Asterisk) = **Reverse** (The "tail" turn happens first).
## Doubles (D)
| **Notation** | **Actual Input** | **Name**     | **Example** |
| ------------ | ---------------- | ------------ | ----------- |
| $D$          | `LL`             | double left  | ![Mazing Pattern 1](patterns/D.gif)|
| $D'$<br>     | `RR`             | indent right | ![Mazing Pattern 1](patterns/D'.gif)|

## Kink (K)
| **Notation** | **Actual Input** | **Name**   | **Example** |
| ------------ | ---------------- | ---------- | ----------- |
| $K$          | `LR`             | Kink left  | ![Mazing Pattern 1](patterns/K.gif)|
| $K'$<br>     | `RL`             | Kink right | ![Mazing Pattern 1](patterns/K'.gif)|

## Bumps (B)
| **Notation** | **Actual Input** | **Name**   | **Example** |
| ------------ | ---------------- | ---------- | ----------- |
| $B$          | `LRRL`           | Bump left  | ![Mazing Pattern 1](patterns/B.gif)|
| $B'$<br>     | `RLLR`           | Bump right | ![Mazing Pattern 1](patterns/B'.gif)|
## The Corners (I/O)
- **Indented Corner (I):** `LRL` or `RLR`.
    - _Concept:_ You "tuck" the corner inward.
- **Out-dented Corner (O):** `LRRRL` or `RLLLR`.
    - _Concept:_ You "bulge" the corner outward.

| **Notation** | **Actual Input** | **Name**     | **Example** |
| ------------ | ---------------- | ------------ | ----------- |
| $I$          | `LRL`            | indent left  | ![Mazing Pattern 1](patterns/I.gif)|
| $I'$<br>     | `RLR`            | indent right | ![Mazing Pattern 1](patterns/I'.gif)|
| $O$          | `RLLLR`          | bulge left   | ![Mazing Pattern 1](patterns/O.gif)|
| $O'$         | `LRRRL`          | bulge right  | ![Mazing Pattern 1](patterns/O'.gif)|
## The Triple Example
### 1. Timing Notation: Queues vs. Manuals
Everything is built from **L** (Left) and **R** (Right). But the _time_ between them matters.
We can borrow a bit of musical or fighting game notation to represent the rhythm:

- **`.` (Dot):** Represents a **Queued** turn (exactly 100ms or `cycle_delay`).
- **`+` (Plus):** Represents a **Delayed/Manual** turn (100ms + ).
- **Standard Triple (T):** `L.L.L.R` (All turns can be queued)
- **Reverse Triple (T′):** `L.R.R+R` (That last turn has to be manual to create a safety margin gap, the rest can be queued).

| **Notation** | **Actual Input** | **Name**               | **Example** |
| ------------ | ---------------- | ---------------------- | ----------- |
| $T$          | `L.L.L.R`        | Triple (Left)          | ![Mazing Pattern 1](patterns/T.gif)|
| $T'$<br>     | `R.R.R.L`        | Triple (Right)         | ![Mazing Pattern 1](patterns/T'.gif)|
| $T*$         | `L.R.R+R`        | Reverse Triple (Left)  | ![Mazing Pattern 1](patterns/T*.gif)|
| $T*'$<br>    | `R.L.L+L`        | Reverse Triple (Right) | ![Mazing Pattern 1](patterns/T*'.gif)|
