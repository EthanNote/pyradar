class Target:
    def __init__(self, position={'x':None, 'y':None}, 
                 velocity={'vx':None, 'vy':None}, 
                 time=None,               
                 device=None,
                 rational_velocity=None,
                 transformed_pos=None,
                 filtered_pos=None):
        self.position=position
        self.velocity=velocity
        self.time=time
        self.rational_velocity=rational_velocity
        self.device=device
        self.transformed_pos=transformed_pos
        self.filtered_pos=filtered_pos