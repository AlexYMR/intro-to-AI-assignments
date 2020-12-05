import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

from copy import deepcopy
import math

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth):
        super(MinimaxPlayer, self).__init__(symbol)
        self.maxDepth = depth
        self.currentDepth = 0
        #depth: maximum number of plies the player will simulate when choosing a move
    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        # use super(MinimaxPlayer,self,board,self.symbol).h1 as evaluation function
        def decision(board,moves):
            cloneBoard = deepcopy(board)
            optimalMove = moves[0]
            optimalEval = NEG_INF
            for move in moves:
                newBoard = game_rules.makeMove(cloneBoard,move)
                val = minimax(newBoard,1,False) #send with depth 1, as this is depth 0, the root
                if val > optimalEval: #final max check
                    optimalMove = move
                    optimalEval = val
            return optimalMove
        
        # recursive function that simulates playing the max
        # (finds best move for self), or playing the min
        # (finds the best move for opponent)
        def minimax(board,currentDepth,isOdd):
            # Note: bool isOdd basically tells us we want the max

            #checking this here REALLY boosts efficiency (due to getLegalMoves getting skipped)
            if currentDepth == self.maxDepth:
                return super(MinimaxPlayer,self).h1(board,self.symbol)

            moves = None
            if isOdd:
                moves = game_rules.getLegalMoves(board,self.symbol)
            else:
                symbol = 'x' if self.symbol == 'o' else 'o'
                moves = game_rules.getLegalMoves(board,symbol)

            # check for end state
            if len(moves) == 0:
                return super(MinimaxPlayer,self).h1(board,self.symbol)
            
            # want max
            if isOdd:
                optimalEval = NEG_INF
                for move in moves:
                    newBoard = game_rules.makeMove(board,move)
                    optimalEval = max(optimalEval,minimax(newBoard,currentDepth+1,False))
                return optimalEval
            # want min
            else:
                optimalEval = POS_INF
                for move in moves:
                    newBoard = game_rules.makeMove(board,move)
                    optimalEval = min(optimalEval,minimax(newBoard,currentDepth+1,True))
                return optimalEval

        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0:
            return decision(board,legalMoves)
        else: return None



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth):
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.maxDepth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        # use super(MinimaxPlayer,self,board,self.symbol).h1 as evaluation function
        def decision(board,moves):
            cloneBoard = deepcopy(board) # clone used for simulation
            optimalMove = moves[0]
            alpha = NEG_INF
            beta = POS_INF
            for move in moves:
                newBoard = game_rules.makeMove(cloneBoard,move)
                val = alphabeta(newBoard,1,False,alpha,beta) #send with depth 1, as this is depth 0, the root
                if val > alpha: #final max check
                    optimalMove = move
                    alpha = val
            return optimalMove
        
        # recursive function that simulates playing the max
        # (finds best move for self), or playing the min
        # (finds the best move for opponent)
        def alphabeta(board,currentDepth,isOdd,alpha,beta):
            # Note: bool isOdd basically tells us we want the max

            #checking this here REALLY boosts efficiency (due to getLegalMoves getting skipped)
            if currentDepth == self.maxDepth:
                return super(AlphaBetaPlayer,self).h1(board,self.symbol)

            moves = None
            symbol = None
            if isOdd:
                moves = game_rules.getLegalMoves(board,self.symbol)
            else:
                symbol = 'x' if self.symbol == 'o' else 'o'
                moves = game_rules.getLegalMoves(board,symbol)

            # check for end state
            if len(moves) == 0:
                # so actually, I ran this using self.h1 and super(...).h1, and super gave me quicker test results... weird
                return super(AlphaBetaPlayer,self).h1(board,self.symbol)
            
            # want max
            if isOdd:
                loc_alpha = alpha
                for move in moves:
                    # check if b <= a; if so exit loop
                    if beta <= loc_alpha:
                        return loc_alpha
                    newBoard = game_rules.makeMove(board,move)
                    loc_alpha = max(loc_alpha,alphabeta(newBoard,currentDepth+1,False,loc_alpha,beta))
                return loc_alpha
            # want min
            else:
                loc_beta = beta
                for move in moves:
                    # check if b <= a; if so exit loop
                    if loc_beta <= alpha:
                        return loc_beta
                    newBoard = game_rules.makeMove(board,move)
                    loc_beta = min(loc_beta,alphabeta(newBoard,currentDepth+1,True,alpha,loc_beta))
                return loc_beta

        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0:
            return decision(board,legalMoves)
        else: return None


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
