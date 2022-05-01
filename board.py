
class Board:
    def __init__(self, name, type, price, house_price, total_houses, rent_prices, mortgage_price, cur_owner, is_mortgaged):
        self.name = name  # the name of the position of the board
        self.type = type  # the color of the position
        self.price = price  # the price to buy the position
        self.house_price = house_price  # the price to buy a house at the position
        self.total_houses = 0  # the total number of houses/hotels currently at this position
        self.rent_prices = rent_prices  # the price of rent depending on total houses at the position
        self.mortgage_price = mortgage_price  # the mortgage price
        self.cur_owner = cur_owner  # the player who currently owns the position on the board
        # if no one owns the position, then it belongs to the bank
        self.is_mortgaged = is_mortgaged  # boolean value on whether position is mortgaged

# position, color, position_price, house_price, total_houses, rent_prices, mortgage, cur_owner, isMortgaged


chance_cards = ["Advance to Boardwalk", "Advance to Go (Collect $200)", "Advance to Illinois Avenue",
                "Advance to St. Charles Place", "Advance to the nearest Railroad",
                "Advance to the nearest Railroad", "Advance token to nearest Utility",
                "Bank pays you dividend of $50", "Get Out of Jail Free", "Go Back 3 Spaces",
                "Go to Jail", "Make general repairs on all your property", "Speeding fine",
                "Take a trip to Reading Railroad", "You have been elected Chairman of the Board",
                "Your building loan matures. Collect $150"]

community_cards = ["Advance to Go (Collect $200)", "Life Insurance Matures",
                   "You have won second prize in a beauty contest", "Bank Error In Your Favor",
                   "From Sale of Stock You Get $45", "Income Tax Refund",
                   "Receive for Services $25", "Get Out of Jail Free", "You Inherit $100",
                   "Go to Jail", "Xmas Fund Matures", "Grand Opera Opening",
                   "Doctor's Fee", "Pay Hospital", "Pay School Tax of $150",
                   "You are Assessed for Street Repairs"]

from xml.sax import xmlreader
import board as info


def cards_and_positions():

        go = info.Board("Go", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)
        # Go position (Collect $200.00)

        med_ave = info.Board("Mediterranean Avenue", "Brown", 60, 50, 0, {0:2, 1:10, 2:30, 3:90, 4:160, 5:250}, 30, "Bank", False)
        # Mediterranean Avenue position ($60) [Mortgage value - $30] [Hotels and houses - $50 each]
        # [Rent $2] [Rent with 1 house - $10] [Rent with 2 houses - $30]
        # [Rent with 3 houses - $90] [Rent with 4 house - $160][Rent with hotel - $250)]

        comm_chest = info.Board("Community Chest", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)
        # Community Chest - follow instructions of card
        # Cards can be: Advance to Go(Collect $200), Life Insurance Matures(Collect $100),
        # You have won second prize in a beauty contest(Collect $10),
        # Bank Error In Your Favor (Collect $200), From Sale of Stock You Get $45,
        # Income Tax Refund(Collect $20), Receive for Services $25),
        # You Inherit $100, Xmas Fund Matures(Collect $100), Grand Opera Opening(Collect $50 from Every Player),
        # Doctor's Fee(Pay $50), Pay Hospital $100,
        # Pay School Tax of $150, You are Assessed for Street Repairs($40 Per House; $115 Per Hotel),
        # Go to Jail, Get Out of Jail Free

        baltic_ave = info.Board("Baltic Avenue", "Brown", 60, 50, 0, {0:4, 1:20, 2:60, 3:180, 4:320, 5:450}, 30, "Bank", False)
        # Baltic Avenue position($60) [Mortgage value - $30] [Hotels and houses - $50 each]
        # [Rent $4] [Rent with 1 house - $20] [Rent with 2 houses - $60] [Rent with 3 houses - $180]
        # [Rent with 4 house - $320] [Rent with hotel - $450)]

        income_tax = info.Board("Income Tax", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)
        # Income Tax position (Pay 10% or $200)
        reading_rr =  info.Board("Reading Railroad", "Railroad", 200, "NULL", "NULL", "NULL", 100, "Bank", False)
        # Reading Railroad ($200) [Mortgage value - $100]
        # [Rent $25] [Rent with 2 R.R.'s - $50] [Rent with 3 R.R.'s - $100] [Rent with 4 R.R.'s - $200]

        orient_ave = info.Board("Oriental Avenue", "Light Blue", 100, 50, 0, {0:6, 1:30, 2:90, 3:270, 4:400, 5:550}, 50, "Bank", False)
        # Oriental Avenue position ($100) [Mortgage value - $50] [Hotels and houses - $50 each]
        # [Rent $6] [Rent with 1 house - $30] [Rent with 2 houses - $90]
        # [Rent with 3 houses - $270] [Rent with 4 house - $400][Rent with hotel - $550)]

        vt_ave = info.Board("Vermont Avenue", "Light Blue", 100, 50, 0, {0:6, 1:30, 2:90, 3:270, 4:400, 5:550}, 50, "Bank", False)
        # Vermont Avenue position ($100) [Mortgage value - $50]
        # [Rent $6] [Rent with 1 house - $30] [Rent with 2 houses - $90]
        # [Rent with 3 houses - $270] [Rent with 4 house - $400][Rent with hotel - $550)]

        ct_ave = info.Board("Connecticut Avenue", "Light Blue", 120, 60, 0, {0:8, 1:40, 2:100, 3:300, 4:450, 5:600}, 60, "Bank", False)
        # Connecticut Avenue position ($120) [Mortgage value - $60]
        # [Rent $8] [Rent with 1 house - $40] [Rent with 2 houses - $100]
        # [Rent with 3 houses - $300] [Rent with 4 house - $450][Rent with hotel - $600)]

        jail = info.Board("Jail", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)
        # In Jail/Jail visiting position

        st_charles = info.Board("St. Charles Place", "Pink", 140, 70, 0, {0:10, 1:50, 2:150, 3:450, 4:625, 5:750}, 70, "Bank", False)
        # St. Charles Place position ($140) [Mortgage value - $70]
        # [Rent $10] [Rent with 1 house - $50] [Rent with 2 houses - $150]
        # [Rent with 3 houses - $450] [Rent with 4 house - $625][Rent with hotel - $750)]

        elec_company = info.Board("Electric Company", "Utility", 150, "NULL", "NULL", "NULL", 75, "Bank", False)
        # Electric Company position ($150) [Mortgage value - $75]

        state_ave = info.Board("States Avenue", "Pink", 140, 100, 0, {0:10, 1:50, 2:150, 3:450, 4:625, 5:750}, 60, "Bank", False)
        # States Avenue position ($140) [Mortgage value - $70] [Hotels and houses - $100 each]
        # [Rent $10] [Rent with 1 house - $50] [Rent with 2 houses - $150]
        # [Rent with 3 houses - $450] [Rent with 4 house - $625][Rent with hotel - $750)]

        va_ave = info.Board("Virginia Avenue", "Pink", 160, 100, 0, {0:8, 1:40, 2:100, 3:300, 4:450, 5:600}, 80, "Bank", False)
        # Virginia Avenue position ($160) [Mortgage value - $80]
        # [Rent $12] [Rent with 1 house - $60] [Rent with 2 houses - $180]
        # [Rent with 3 houses - $500] [Rent with 4 house - $700][Rent with hotel - $900)]

        pa_rr = info.Board("Pennsylvania Railroad", "Railroad", 200, "NULL", "NULL", "NULL", 100, "Bank", False)
        # Pennsylvania Railroad position ($200) [Mortgage value - $100]
        # [Rent $25] [Rent with 2 R.R.'s - $50] [Rent with 3 R.R.'s - $100] [Rent with 4 R.R.'s - $200]

        st_james = info.Board("St. James Place", "Orange", 180, 100, 0, {0:14, 1:70, 2:200, 3:550, 4:750, 5:950}, 90, "Bank", False)
        # St. James Place position ($180) [Mortgage value - $90]
        # [Rent $14] [Rent with 1 house - $70] [Rent with 2 houses - $200]
        # [Rent with 3 houses - $550] [Rent with 4 house - $750][Rent with hotel - $950)]

        tn_ave = info.Board("Tennessee Avenue", "Orange", 180, 100, 0, {0:14, 1:70, 2:200, 3:550, 4:750, 5:950}, 90, "Bank", False)
        # Tennessee Avenue position ($180) [Mortgage value - $90]
        # [Rent $14] [Rent with 1 house - $70] [Rent with 2 houses - $200]
        # [Rent with 3 houses - $550] [Rent with 4 house - $750][Rent with hotel - $950)]

        ny_ave = info.Board("New York Avenue", "Orange", 200, 100, 0, {0:16, 1:80, 2:220, 3:600, 4:800, 5:1000}, 100, "Bank", False)
        # New York Avenue position ($200) [Mortgage value - $100]
        # [Rent $16] [Rent with 1 house - $80] [Rent with 2 houses - $220]
        # [Rent with 3 houses - $600] [Rent with 4 house - $800][Rent with hotel - $1000)]

        free_parking = info.Board("Free Parking", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)
        # Free Parking position

        ky_ave = info.Board("Kentucky Avenue", "Red", 220, 150, 0, {0:18, 1:90, 2:250, 3:700, 4:875, 5:1050}, 110, "Bank", False)
        # Kentucky Avenue position ($220) [Mortgage value - $110]
        # [Rent $18] [Rent with 1 house - $90] [Rent with 2 houses - $250]
        # [Rent with 3 houses - $700] [Rent with 4 house - $875][Rent with hotel - $1050)]

        in_ave = info.Board("Indiana Avenue", "Red", 220, 150, 0, {0:18, 1:90, 2:250, 3:700, 4:875, 5:1050}, 110, "Bank", False)
        # Indiana Avenue position ($220) [Mortgage value - $110]
        # [Rent $18] [Rent with 1 house - $90] [Rent with 2 houses - $250]
        # [Rent with 3 houses - $700] [Rent with 4 house - $875][Rent with hotel - $1050)]

        il_ave = info.Board("Illinois Avenue", "Red", 240, 150, 0, {0:20, 1:100, 2:300, 3:750, 4:925, 5:1100}, 120, "Bank", False)
        # Illinois Avenue position ($240) [Mortgage value - $120]
        # [Rent $20] [Rent with 1 house - $100] [Rent with 2 houses - $300]
        # [Rent with 3 houses - $750] [Rent with 4 house - $925][Rent with hotel - $1100)]

        bo_rr = info.Board("B. & O. Railroad", "Railroad", 200, "NULL", "NULL", "NULL", 100, "Bank", False)
        # B. & O. Railroad position ($200) [Mortgage value - $100]
        # [Rent $25] [Rent with 2 R.R.'s - $50] [Rent with 3 R.R.'s - $100] [Rent with 4 R.R.'s - $200]

        atlantic_ave = info.Board("Atlantic Avenue", "Yellow", 260, 150, 0, {0:22, 1:110, 2:330, 3:800, 4:975, 5:1150}, 130, "Bank", False)
        # Atlantic Avenue position ($260) [Mortgage value - $130]
        # [Rent $22] [Rent with 1 house - $110] [Rent with 2 houses - $330]
        # [Rent with 3 houses - $800] [Rent with 4 house - $975][Rent with hotel - $1150)]

        ventnor_ave = info.Board("Ventnor Avenue", "Yellow", 260, 150, 0, {0:22, 1:110, 2:330, 3:800, 4:975, 5:1150}, 130, "Bank", False)
        # Ventnor Avenue position ($260) [Mortgage value - $130]
        # [Rent $22] [Rent with 1 house - $110] [Rent with 2 houses - $330]
        # [Rent with 3 houses - $800] [Rent with 4 house - $975][Rent with hotel - $1150)]

        water_works = info.Board("Water Works", "Utility", 150, "NULL", "NULL", "NULL", 75, "Bank", False)
        # Water Works position ($150) [Mortgage value - $75.00]

        marvin_gardens = info.Board("Marvin Gardens", "Yellow", 280, 150, 0, {0:24, 1:120, 2:360, 3:850, 4:1025, 5:1200}, 140, "Bank", False)
        # Marvin Gardens position ($280) [Mortgage value - $140]
        # [Rent $24] [Rent with 1 house - $120] [Rent with 2 houses - $360]
        # [Rent with 3 houses - $850] [Rent with 4 house - $1025][Rent with hotel - $1200)]

        go_to_jail = info.Board("Go to Jail", "NULL" , "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)

        pacific_ave = info.Board("Pacific Avenue", "Green", 300, 200, 0, {0:26, 1:130, 2:390, 3:900, 4:1100, 5:1275}, 150, "Bank", False)
        # Pacific Avenue position ($300) [Mortgage value - $150]
        # [Rent $26] [Rent with 1 house - $130] [Rent with 2 houses - $390]
        # [Rent with 3 houses - $900] [Rent with 4 house - $1100][Rent with hotel - $1275)]

        nc_ave = info.Board("North Carolina Avenue", "Green", 300, 200, 0, {0:26, 1:130, 2:390, 3:900, 4:1100, 5:1275}, 150, "Bank", False)
        # North Carolina Avenue position ($300) [Mortgage value - $150]
        # [Rent $26] [Rent with 1 house - $130] [Rent with 2 houses - $390]
        # [Rent with 3 houses - $900] [Rent with 4 house - $1100][Rent with hotel - $1275)]

        pa_ave = info.Board("Pennsylvania Avenue", "Green", 320, 200, 0, {0:28, 1:150, 2:450, 3:1000, 4:1200, 5:1400}, 160, "Bank", False)
        # Pennsylvania Avenue position ($320) [Mortgage value - $160]
        # [Rent $28] [Rent with 1 house - $150] [Rent with 2 houses - $450]
        # [Rent with 3 houses - $1000] [Rent with 4 house - $1200][Rent with hotel - $1400)]

        short_line_rr = info.Board("Short Line Railroad", "Railroad", 200, "NULL", "NULL", "NULL", 100, "Bank", False)
        # Short Line Railroad position ($200) [Mortgage value - $100]
        # [Rent $25] [Rent with 2 R.R.'s - $50] [Rent with 3 R.R.'s - $100] [Rent with 4 R.R.'s - $200]

        chance = info.Board("Chance", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)
        # Advance to Boardwalk
        # Advance to Go (Collect $200)
        # Advance to Illinois Avenue. If you pass Go, collect $200
        # Advance to St. Charles Place. If you pass Go, collect $200
        # Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled
        # Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled
        # Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown.
        # Bank pays you dividend of $50
        # Get Out of Jail Free
        # Go Back 3 Spaces
        # Go to Jail. Go directly to Jail, do not pass Go, do not collect $200
        # Make general repairs on all your property. For each house pay $25. For each hotel pay $100
        # Speeding fine $15
        # Take a trip to Reading Railroad. If you pass Go, collect $200
        # You have been elected Chairman of the Board. Pay each player $50
        # Your building loan matures. Collect $150

        park_place = info.Board("Park Place", "Dark Blue", 350, 200, 0, {0:35, 1:175, 2:500, 3:1100, 4:1300, 5:1500}, 175, "Bank", False)
        # Park Place position ($350) [Mortgage value - $175]
        # [Rent $35] [Rent with 1 house - $175] [Rent with 2 houses - $500]
        # [Rent with 3 houses - $1100] [Rent with 4 house - $1300][Rent with hotel - $1500)]

        luxury_tax = info.Board("Luxury Tax", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "Bank", False)
        # Luxury Tax position (Pay $75.00)
        # [Rent $6] [Rent with 1 house - $30] [Rent with 2 houses - $90]
        # [Rent with 3 houses - $270] [Rent with 4 house - $400][Rent with hotel - $550)]

        boardwalk = info.Board("Boardwalk", "Dark Blue", 400, 200, 0, {0:50, 1:200, 2:600, 3:1400, 4:1700, 5:2000}, 200, "Bank", False)
        # Boardwalk position ($400) [Mortgage value - $200]
        # [Rent $50] [Rent with 1 house - $200] [Rent with 2 houses - $600]
        # [Rent with 3 houses - $1400] [Rent with 4 house - $1700][Rent with hotel - $2000)]


        board = [go, med_ave, comm_chest, baltic_ave, income_tax, reading_rr, orient_ave, chance, vt_ave, ct_ave, jail,
        st_charles, elec_company, state_ave, va_ave, pa_rr, st_james, comm_chest, tn_ave, ny_ave, free_parking,
        ky_ave, chance, in_ave, il_ave, bo_rr, atlantic_ave, ventnor_ave, water_works, marvin_gardens,
        go_to_jail, pacific_ave, nc_ave, comm_chest, pa_ave, short_line_rr, chance, park_place,
        luxury_tax, boardwalk]
        return board


