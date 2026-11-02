class PoseDistance:
    def __init__(self, pose, distance):
        """
        Stores a pose and its distance from the center of the frame.
        
        Args:
            pose: List of Point containing pose keypoints
            distance: distance from the center of the frame
        """
        
        self.__pose = pose
        self.__distance = distance
    
    def __lt__(self, other):
        """
        Comparison function used for sorting.
        
        Args:
            other: PoseDistance, pose to compare to.
        """
        
        return self.__distance < other.__distance
    
    @property
    def pose(self):
        return self.__pose