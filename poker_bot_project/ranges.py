from range import Range

rec_ranges = {
    'limp': Range(['A2o+','K4o+','Q6o+','J7o+','T7o+','97o+','22+','A2s+','K2s+','Q2s+','J3s+','T6s+','96s+','86s+','75s+','65s','54s']),
    '15%': Range(0.4),
    '30%': Range(0.2),
}

reg_ranges = {
    'limp': Range(0.4),
    '15%': Range(0.2),
    '30%': Range(0.09),
}

bot_open_ranges = {
    '50BB': {
        'UTG':{
            'raise': Range(0.118)
        },
        'UTG+1': {
            'raise': Range(0.136)
        },
        'LJ': {
            'raise': Range(0.166)
        },
        'HJ': {
            'raise': Range(0.197)
        },
        'CO': {
            'raise': Range(0.251)
        },
        'BTN': {
            'raise': Range(0.36)
        },
        'SB': {
            'raise': Range(0.14),
            'limp': Range(0.55)
        },
    },
    '17BB': {
        'UTG': {
            'raise': Range(0.105)
        },
        'UTG+1': {
            'raise': Range(0.118)
        },
        'LJ': {
            'raise': Range(0.133)
        },
        'HJ': {
            'raise': Range(0.173)
        },
        'CO': {
            'raise': Range(0.213)
        },
        'BTN': {
            'all in': Range(['A7o','A8o','A9o','ATo','KQo','QJo','JTs','Q9s','T9s','55','44','33','A3s','A2s']),
            'raise': Range(0.16),
            'limp': Range(0.26)
        },
        'SB': {
            'all in': Range(['A5o+','K5o','K6o','T7s','97s','87s','76s','55','44','33']),
            'raise': Range(0.2),
            'limp': Range(0.57)
        }
    },
    '10BB': {
        'UTG': {
            'all in': Range(0.1)
        },
        'UTG+1': {
            'all in': Range(0.115)
        },
        'LJ': {
            'all in': Range(0.13)
        },
        'HJ': {
            'all in': Range(0.16)
        },
        'CO': {
            'all in': Range(0.2)
        },
        'BTN': {
            'all in': Range(0.27)
        },
        'SB': {
            'limp': Range(['77+','98s+','T8s+','J8s+','Q8s+','KTs+','AQs+']),
            'all in': Range(0.4)
        }
    }
}

bot_facing_bets_ranges = {
    '50BB': {
        'UTG': {
            '30%': Range(0.06),
            '100%': Range(0.03)
        },
        'UTG+1': {
            '30%': Range(0.05),
            '10%': Range(0.09),
            '100%': Range(0.03)
        },
        'LJ': {
            '30%': Range(0.055),
            '10%': Range(0.1),
            '100%': Range(0.03)
        },
        'HJ': {
            '30%': Range(0.06),
            '10%': Range(0.11),
            '100%': Range(0.03)
        },
        'CO': {
            '30%': Range(0.065),
            '10%': Range(0.12),
            '100%': Range(0.03)
        },
        'BTN': {
            '30%': Range(0.07),
            '10%': Range(0.15),
            '100%': Range(0.03)
        },
        'SB': {
            '30%': Range(0.075),
            '10%': Range(0.13),
            '100%': Range(0.03)
        },
        'BB': {
            '30%': Range(0.08),
            '10%': Range(0.4),
            '100%': Range(0.03)
        }
    },

    '17BB': {
        'UTG': {
            '100%': Range(0.04)
        },
        'UTG+1': {
            '20%': Range(0.07),
            '100%': Range(0.04)
        },
        'LJ': {
            '100%': Range(0.045),
            '20%': Range(0.08)
        },
        'HJ': {
            '100%': Range(0.05),
            '20%': Range(0.09)
        },
        'CO': {
            '100%': Range(0.055),
            '20%': Range(0.1)
        },
        'BTN': {
            '100%': Range(0.06),
            '20%': Range(0.12)
        },
        'SB': {
            '100%': Range(0.065),
            '20%': Range(0.14)
        },
        'BB': {
            '100%': Range(0.07),
            '20%': Range(0.55)
        }

    },

    '10BB': {
        'UTG+1': {
            '100%': Range(0.06)
        },
        'LJ': {
            '100%': Range(0.065)
        },
        'HJ': {
            '100%': Range(0.07)
        },
        'CO': {
            '100%': Range(0.075)
        },
        'BTN': {
            '100%': Range(0.08)
        },
        'SB': {
            '100%': Range(0.085),
            '20%': Range(0.15)
        },
        'BB': {
            '100%': Range(0.09),
            '20%': Range(1)
        }
    }
}