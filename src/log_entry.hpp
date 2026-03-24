#pragma once

struct LogEntry {
    uint64_t timestamp_ns;
    uint32_t order_id;
    char symbol[8];
    double price;
    int32_t quantity;
    char side;
};