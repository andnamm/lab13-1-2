"""
File: linkedbst.py
Author: Ken Lambert
"""

import random
from math import log
import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        self._last = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            msg = ""
            if node is not None:
                msg += recurse(node.right, level + 1)
                msg += "| " * level
                msg += str(node.data) + "\n"
                msg += recurse(node.left, level + 1)
            return msg

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.right is None and top.left is None:
                return 0

            left_sum = height1(top.left) if top.left is not None else -1
            right_sum = height1(top.right) if top.right is not None else -1
            return max(left_sum, right_sum) + 1

        return height1(self._root)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        els = self._size
        return self.height() < (2 * log(els + 1) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        els_inorder = [el for el in self.inorder()]
        return [el for el in els_inorder if el in range(low, high + 1)]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        els_inorder = [el for el in self.inorder()]
        els_inorder = self.inorder()

        def rebalance(els):
            if len(els) == 0:
                return None

            index = len(els) // 2

            node = BSTNode(els[index])
            node.left = rebalance(els[:index])
            node.right = rebalance(els[index + 1:])

            return node

        self._root = rebalance(list(els_inorder))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        els_inorder = [el for el in self.inorder()]
        for elem in els_inorder:
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        els_inorder = [el for el in self.inorder()]
        for elem in els_inorder[::-1]:
            if elem < item:
                return elem
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path: path to a words file
        :type path: str
        :return: time efficiency of 4 programs
        :rtype: str
        """
        words = self._read_file(path)
        words_shuffle = words.copy()
        random.shuffle(words_shuffle)
        print('Running ...')

        ## 10_000 words search in a list using list methods
        start = time.time()
        self._search_in_list(words, words_shuffle[:10000])
        end = time.time()

        time1 = end - start
        print('Running 1/4')

        words1 = [x.lower() for x in words]                  # solves the uppercase problem so find method not return None
        words_shuffle1 = [x.lower() for x in words_shuffle]  # as ord('a')>ord('c')which is not counted in the words.txt
        words_tree_alphabetical = self._words_to_tree(words1, 'alphabetical')

        ## 10_000 words search in a alphbetically ordered words list implemented as a binary tree
        start = time.time()
        for word in words_shuffle1[:10_000]:
            words_tree_alphabetical.find_iterative(word)
        end = time.time()

        time2 = end - start
        print('Running 2/4')

        random_words_copy = words.copy()
        random.shuffle(random_words_copy)
        words_tree_random = self._words_to_tree(random_words_copy)

        # 10_000 words search in a randomly ordered words list implemented as a binary tree
        start = time.time()
        for word in words_shuffle[:10_000]:
            words_tree_random.find(word)
            # words_tree_random.find_iterative(word)
        end = time.time()

        time3 = end - start
        print('Running 3/4')

        words_tree_random.rebalance()
        ## 10_000 words search in a randomly ordered words list implemented as balanced binary tree
        start = time.time()
        for word in words_shuffle[:10_000]:
            words_tree_random.find(word)
            # words_tree_random.find_iterative(word)
        end = time.time()

        time4 = end - start
        print('Running 4/4')
        print()

        return f'Search using list execution time = {time1}\n' \
               f'Search in alphbetically ordered tree execution time = {time2}\n' \
               f'Search in randomly ordered tree execution time = {time3}\n' \
               f'Search in randomly ordered balanced tree execution time = {time4}\n'


    def find_iterative(self, item):
        """Iteratively checks if item matches an item in a tree.
        If yes returns the matched item, or None otherwise.

        Args:
            item (str): item to search for

        Returns:
            str: matched item in a tree
            None: item not found
        """
        node = self._root
        while node is not None:

            if item == node.data:
                return node.data
            elif item > node.data:
                node = node.right
            else:
                node = node.left
        return None

    @staticmethod
    def _read_file(path):
        """Reads a file and lists all words

        Args:
            path (str): a path to a file to read

        Returns:
            list: list of words
        """
        with open(path) as file:
            contents = file.read()
        return contents.split()

    @staticmethod
    def _search_in_list(words, list_to_find):
        """Finds all apearances of list_to_find elements in words.

        Args:
            words (list): a list to search in
            list_to_find (list): list of elements to find

        Returns:
            list: found words
        """
        found_words = []

        for word in list_to_find:
            if word in words:
                found_words.append(word)
            else:
                print(word, None)

        return words

    @staticmethod
    def _words_to_tree(words, type=None):
        """Converts a list into a tree.

        Args:
            words (list): words to convert
            type (str, optional): type='alphabetical' to convert an alphabetically ordered list.

        Returns:
            LinkedBST: resulted tree of words.
        """
        # print('Converting words file to a tree')
        words_bt = LinkedBST()
        if type == 'alphabetical':
            for word in words:
                words_bt.insert_right(word)

        else:
            for word in words:
                words_bt.add(word)

        return words_bt

    def insert_right(self, data):
        """Adds a node only right to the tree.

        Args:
            data (any): data to add
        """
        node = BSTNode(data)
        if self._root is None:
            self._root = node
            self._last = node

        else:
            self._last.right = node
            self._last = self._last.right

        self._size += 1

if __name__ == "__main__":
    lbst = LinkedBST()

    # for j in sorted([113, 30, 68, 74, 45, 91, 88]):
    #     lbst.add(j)
    # print(lbst)
    # print(lbst.height())
    # print(lbst.is_balanced())
    # lbst.rebalance()
    # print(lbst)
    # print(lbst.is_balanced())
    # print(lbst.predecessor(15))
    # print(lbst.range_find(30, 91))

    file = '/mnt/d/programming/2022/lab13/binary_search_tree/words.txt'
    print(lbst.demo_bst(file))
    