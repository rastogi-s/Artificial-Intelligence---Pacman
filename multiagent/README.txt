####################################################################################################
####################################        HOMEWORK 2        ######################################
####################################################################################################



 > Goal: Q1 -> Write a evaluation function for Pacman (ReflexAgent)
 		 Q5 -> Write a evaluation function for Pacman (ExpectimaxAgent)
 		
 > Time Spent on the assignment : 15 hrs
 
 > Details about the evaluation functions:
 
 	> Q1. For calculation of score we consider four factors 
 			1. closest food distance from the new position
 			2. Ghost distance from the new position.
 			3. Action ( in case of new position is a wall (STOP))
 			4. closest power capsules.  
 	
 		Considering above mentioned factors the score is evaluated as follows.
 		1. We subtract the minimum food distance from the score. So that the new position having
 		   greater minimum food distance will have a much lower score.
 		2. We check the distance of all ghosts from the new position and if the distance of any 
 		   ghost is less than 1 then, the new position could lead pacman to lose the game, hence
 		   we give the lowest possible score for that position.
 		3. If the new action is STOP , then the position is not viable for pacman hence giving a 
 		   negative value for that action.
 		4. We calculate the distance of the closest power capsule from the new position and if 
 		   the distance is zero (which is the most desired position ) we assign a highest 
 		   possible score for that position and if the distance is not zero we add the reciprocal 
 		   of the minimum distance to the score.(position with greater 
 		   distance will have lesser score)  
 		
 	
 	> Q5. For calculation of score we consider three factors 
 			1. food distance from the current position
 			2. Ghost distance from the current position and its scared time.
 			3. closest power capsules.  
 	
 		Considering above mentioned factors the score is evaluated as follows.
 		1. We calculate the maximum of the reciprocal of distances of each food positions from
 		   the current position. (i.e. the current position which is closest to a food item will 
 		   have maximum reciprocal distance.) and add it to the score.
 		2. If the ghost has a scared time greater than zero, we add the reciprocal of distance of
 		   each ghost from the current position otherwise subtract the same from the score.
 		3. We calculate the maximum of reciprocal of distance of power capsule from the current 
 		   position and add it to the score
 		4. Also we can use the actual currentgameState score that is displayed on the screens.
 		   
 		   