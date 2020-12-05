import game_manager, game_rules, unittest
from player import makePlayer
from multiprocessing.pool import ThreadPool

def run_test(gm):
    gm.play()
    game_rules.printBoard(gm.board)
    print(gm.GetWinner(), "WINS")
    return gm.board

class GameTest(unittest.TestCase):

    def makeGame(self, size, player1, player2, depth, script=None):
        gm = game_manager.GameManager(
              size
            , size
            , makePlayer(player1, 'x', depth)
            , makePlayer(player2, 'o', depth)
            , script
            , True)
        return gm

    def test1(self):
        p1 = 'm'
        p2 = 'd'
        depth = 2
        gm = self.makeGame(4, p1, p2, depth)

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(300)
            print("Supposed to look like:")
            game_rules.printBoard([['x', ' ', ' ', 'o'], [' ', 'x', ' ', 'x'], [' ', 'o', ' ', 'o'], ['o', 'x', 'o', 'x']])
            self.assertEqual(gm.board,
                                [['x', ' ', ' ', 'o'], [' ', 'x', ' ', 'x'], [' ', 'o', ' ', 'o'], ['o', 'x', 'o', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))


    def test1s(self):
        # Identical to test1 but totally run by the game1.log script
        # Minimax player never gets called.
        # Truncate game1.log to script the early game play and Minimax for rest
        p1 = 'm'
        p2 = 'd'
        depth = 2
        gm = self.makeGame(4, p1, p2, depth, 'game1.log')

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(300)
            self.assertEqual(gm.board,
                             [['x', ' ', ' ', 'o'], [' ', 'x', ' ', 'x'], [' ', 'o', ' ', 'o'], ['o', 'x', 'o', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))


    def test2(self):
        p1 = 'm'
        p2 = 'd'
        depth = 5
        gm = self.makeGame(4, p1, p2, depth)

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(300)
            self.assertEqual(gm.board,
                             [['x', ' ', ' ', 'o'], [' ', 'x', ' ', 'x'], [' ', 'o', ' ', 'o'], ['o', 'x', 'o', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))


    def test3(self):
        p1 = 'd'
        p2 = 'm'
        depth = 4
        gm = self.makeGame(6, p1, p2, depth)

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(300)
            self.assertEqual(gm.board, [[' ', 'o', ' ', 'o', ' ', 'o'], [' ', ' ', ' ', ' ', ' ', ' '],
                                        [' ', ' ', ' ', ' ', 'x', ' '], ['o', ' ', ' ', 'x', 'o', 'x'],
                                        [' ', ' ', 'x', ' ', 'x', 'o'], ['o', 'x', 'o', 'x', 'o', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))


    def test4(self):
        # Uses script to have alternative start moves
        p1 = 'm'
        p2 = 'd'
        depth = 6
        gm = self.makeGame(4, p1, p2, depth, 'game4.log')

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(300)
            self.assertEqual(gm.board,
                             [['x', ' ', ' ', 'o'], ['o', ' ', ' ', 'x'], ['x', 'o', 'x', 'o'], ['o', ' ', ' ', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))


    def test5(self):
        p1 = 'd'
        p2 = 'a'
        depth = 4
        gm = self.makeGame(6, p1, p2, depth)

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(300)
            self.assertEqual(gm.board, [[' ', 'o', ' ', 'o', ' ', 'o'], [' ', ' ', ' ', ' ', ' ', ' '],
                                        [' ', ' ', ' ', ' ', 'x', ' '], ['o', ' ', ' ', 'x', 'o', 'x'],
                                        [' ', ' ', 'x', ' ', 'x', 'o'], ['o', 'x', 'o', 'x', 'o', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))


    def test6(self):
        p1 = 'a'
        p2 = 'd'
        depth = 7
        gm = self.makeGame(8, p1, p2, depth)

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(9000)
            self.assertEqual(gm.board,
                             [['x', ' ', 'x', ' ', 'x', ' ', ' ', 'o'], [' ', ' ', ' ', 'x', ' ', ' ', ' ', 'x'],
                              [' ', ' ', 'x', ' ', 'x', ' ', ' ', 'o'], ['o', ' ', ' ', ' ', ' ', 'x', ' ', 'x'],
                              [' ', 'o', ' ', 'o', ' ', ' ', ' ', 'o'], ['o', ' ', 'o', ' ', ' ', ' ', 'o', 'x'],
                              ['x', ' ', ' ', 'o', ' ', 'o', 'x', 'o'], ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))


    def test6s(self):
        # Identical to test6 but completely script driven
        p1 = 'a'
        p2 = 'd'
        depth = 6
        gm = self.makeGame(8, p1, p2, depth, 'game6.log')

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(run_test, [gm])
        result = None
        try:
            returned_value = async_result.get(300)
            self.assertEqual(gm.board,
                             [['x', ' ', 'x', ' ', 'x', ' ', ' ', 'o'], [' ', ' ', ' ', 'x', ' ', ' ', ' ', 'x'],
                              [' ', ' ', 'x', ' ', 'x', ' ', ' ', 'o'], ['o', ' ', ' ', ' ', ' ', 'x', ' ', 'x'],
                              [' ', 'o', ' ', 'o', ' ', ' ', ' ', 'o'], ['o', ' ', 'o', ' ', ' ', ' ', 'o', 'x'],
                              ['x', ' ', ' ', 'o', ' ', 'o', 'x', 'o'], ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x']])
        except Exception as e:
            self.fail('Timed out: {}'.format(e))

    def test7(self):
        #shallow test (on small board) to ensure minimax is returning the proper move @ certain depth w/o running whole game simulation
        #tree has 2 winning moves for X, should choose first one it sees
        #actually passed this before passing test1 due to python version differences, which added to my confusion at the time
        depth = 2
        p1 = makePlayer("m","x",depth)

        board = [
            ["x","o","x","x"],
            ["o","x"," "," "],
            [" ","o"," ","o"],
            [" "," "," ","x"]
        ]
        move = p1.getMove(board)
        self.assertEqual(((0,0),(2,0)),move)

    
    def test8(self):
        #shallow test (on small board) to ensure alphabeta is running faster (& therefore pruning) in comparison to minimax
        depth = 5

        p1 = makePlayer("m","x",depth)
        p2 = makePlayer("a","x",depth)

        board = [
            ["x"," ","x","o","x","o"],
            [" ","x","o","x","o","x"],
            [" ","o","x","o","x","o"],
            ["o","x","o","x","o","x"],
            ["x","o","x","o","x","o"],
            ["o","x","o","x","o","x"]
        ]
        import time as t

        minimaxStartTime = t.time()
        minimaxMove = p1.getMove(board)
        minimaxEndTime = (t.time() - minimaxStartTime)

        alphabetaStartTime = t.time()
        alphabetaMove = p2.getMove(board)
        alphabetaEndTime = (t.time() - alphabetaStartTime)
        
        print("\nminimaxEndTime and alphabetaEndTime differed by: " + str(minimaxEndTime - alphabetaEndTime) + " seconds\n")
        self.assertTrue(minimaxEndTime > alphabetaEndTime)


if __name__== "__main__":
    unittest.main()
