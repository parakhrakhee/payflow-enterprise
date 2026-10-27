-- Reconcile transaction counts and amounts by payment status.
SELECT
    status,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM payment_transactions
GROUP BY status
ORDER BY status;

-- Overall transaction summary.
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount,
    COUNT(*) FILTER (WHERE status = 'COMPLETED') AS completed_count,
    COUNT(*) FILTER (WHERE status = 'PENDING') AS pending_count
FROM payment_transactions;
