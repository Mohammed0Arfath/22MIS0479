# Stage 1 — Notification System Design

## Goal
Select the top `n` (default 10) unread notifications by combining priority (weight) and recency.

## Priority rules
- Weight mapping: Placement > Result > Event (3, 2, 1).
- Recency: newer notifications are preferred when weights tie.

## Approach
1. Assign each notification a numeric `score = weight * 10^12 + epoch_ts` so weight is the dominant factor and recency breaks ties.
2. Maintain a fixed-size min-heap of size `n`. For every incoming notification (streaming), push into the heap; if heap size exceeds `n`, pop the smallest. This ensures O(log n) per insertion and O(n) memory.

## Why this is efficient
- For streaming data, we never store all notifications — only the top `n` candidates.
- Complexity: O(m log n) for m notifications processed. For small n (10), this is effectively linear in m with tiny per-item cost.

## Handling new notifications
Process notifications as they arrive; update heap accordingly. If a new notification outranks current lowest in heap, it replaces it.

## Edge cases
- If timestamp parsing fails, fallback to a low epoch so older.
- Unknown `Type` maps to lowest weight.

## Files
- `priority_inbox.py`: runnable script that authenticates, fetches notifications, and prints top 10.
