/*
 * Copyright (c) 2016 Intel Corporation
 * Copyright (c) 2018 Nordic Semiconductor
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @addtogroup t_driver_wdt
 * @{
 * @defgroup t_wdt_basic test_wdt_basic_operations
 * @}
 */

#include <zephyr/kernel.h>
#include <zephyr/ztest.h>

// #include <zephyr/drivers/watchdog.h>
// #if DT_HAS_COMPAT_STATUS_OKAY(st_stm32_watchdog)
// #define WDT_NODE            DT_INST(0, st_stm32_window_watchdog)

// static void wdt_basic_test_teardown(void *fixture)
// {
//     const struct device *const wdt = DEVICE_DT_GET(WDT_NODE);
//     int err;

//     if (!device_is_ready(wdt)) {
//         return;
//     }

//     err = wdt_disable(wdt);
//     if (err < 0 && err != -EPERM && err != -EFAULT) {
//         TC_PRINT("test teardown: watchdog disable error: %d\n", err);
//     }
//         TC_PRINT("test teardown: watchdog disable successfully\n");

// }

// ZTEST_SUITE(wdt_basic_test_suite, NULL, NULL, NULL, NULL, wdt_basic_test_teardown);
// #else
// ZTEST_SUITE(wdt_basic_test_suite, NULL, NULL, NULL, NULL, NULL);
// #endif

// ZTEST_SUITE(wdt_basic_test_suite, NULL, NULL, NULL, NULL, NULL);
