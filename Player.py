class Player:
    def __init__(self, player_id: int, position: str, name: str, club: str,
                 points: int, price: float, points_per_price: float = 0):
        self.player_id = player_id
        self.position = position
        self.name = name
        self.club = club
        self.points = points
        self.price = price
        self.points_per_price = points_per_price

    def __str__(self):
        return f"{self.player_id} {self.position} {self.name} {self.club} {self.points} {self.price} {self.points_per_price}"

    def __repr__(self):
        return f"{self.player_id}"


