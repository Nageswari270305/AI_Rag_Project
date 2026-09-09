def reciprocal_rank_fusion(
    dense_results,
    bm25_results,
    k=60
):

    scores = {}

    points = {}

    for rank, result in enumerate(
        dense_results
    ):

        point_id = result.id

        scores[point_id] = scores.get(
            point_id,
            0
        ) + 1 / (k + rank + 1)

        points[point_id] = result

    for rank, result in enumerate(
        bm25_results
    ):

        point = result["point"]

        point_id = point.id

        scores[point_id] = scores.get(
            point_id,
            0
        ) + 1 / (k + rank + 1)

        points[point_id] = point

    ranked_ids = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    results = []

    for point_id in ranked_ids:

        results.append({
            "point": points[point_id],
            "score": scores[point_id]
        })

    return results