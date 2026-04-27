# CRF Hyperparameter Tuning

This experiment performs dev-set grid search over CRF regularization parameters `c1` and `c2`.

## Search Space

- c1: 0.01, 0.1, 0.5, 1.0
- c2: 0.01, 0.1, 0.5, 1.0
- Selection metric: development span-level exact-match F1

## Results

| Rank | c1 | c2 | Dev Span P | Dev Span R | Dev Span F1 | Dev Token F1 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.01 | 0.1 | 0.671 | 0.519 | 0.585 | 0.516 |
| 2 | 0.5 | 0.01 | 0.657 | 0.506 | 0.572 | 0.503 |
| 3 | 0.01 | 0.01 | 0.661 | 0.501 | 0.570 | 0.487 |
| 4 | 0.01 | 0.5 | 0.648 | 0.506 | 0.569 | 0.522 |
| 5 | 0.5 | 0.5 | 0.647 | 0.504 | 0.567 | 0.536 |
| 6 | 0.5 | 0.1 | 0.639 | 0.499 | 0.560 | 0.525 |
| 7 | 1.0 | 1.0 | 0.660 | 0.479 | 0.555 | 0.529 |
| 8 | 0.1 | 0.5 | 0.633 | 0.491 | 0.553 | 0.517 |
| 9 | 0.01 | 1.0 | 0.642 | 0.484 | 0.552 | 0.509 |
| 10 | 0.1 | 1.0 | 0.629 | 0.486 | 0.548 | 0.506 |
| 11 | 0.1 | 0.01 | 0.627 | 0.484 | 0.546 | 0.494 |
| 12 | 0.5 | 1.0 | 0.618 | 0.489 | 0.546 | 0.548 |
| 13 | 1.0 | 0.01 | 0.638 | 0.466 | 0.539 | 0.513 |
| 14 | 1.0 | 0.5 | 0.639 | 0.463 | 0.537 | 0.513 |
| 15 | 0.1 | 0.1 | 0.616 | 0.476 | 0.537 | 0.499 |
| 16 | 1.0 | 0.1 | 0.632 | 0.453 | 0.528 | 0.500 |

## Best Configuration

- Best c1: 0.01
- Best c2: 0.1
- Best dev span F1: 0.585
- Best dev token F1: 0.516

## Interpretation

This tuning experiment replaces the earlier fixed-parameter CRF setup with a systematic dev-set grid search. The selected configuration is then retrained on train+dev and evaluated on the held-out test set.