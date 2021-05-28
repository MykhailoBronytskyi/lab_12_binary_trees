"""
File: linkedbst.py
Author: Ken Lambert
"""
import time
import random
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:

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
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""


        current_node = self._root
        curent_data = None


        while True:
            if current_node is None:
                return None
    
            curent_data = current_node.data
            if curent_data == None:
                return None
            elif item < curent_data:
                current_node = current_node.left
            elif item > curent_data:
                current_node = current_node.right
            elif item == curent_data:
                break
        
        return curent_data


    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        def _add_child(parent, item):
            '''Help function for adding a child. The parent must have free brunches'''
            if item < parent.data:
                parent.left == BSTNode(item)
            else:
                parent.right == BSTNode(item)

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            pearent_node = None
            current_node = self._root
            curent_data = None

            while True:
                if current_node is None:
                    _add_child(pearent_node, item)
                    break

                pearent_node = current_node
                # New item is less, go left until spot is found
                if item < current_node.data:
                    current_node = current_node.left
                # New item is greater or equal
                else:
                    current_node = current_node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right

            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, position=None):
        """Return the height of the subtree rooted at Position p.
        If p is None, return the height of the entire tree.
        """
        def height_1(position):
            """Return the height of the subtree rooted at Position p."""
            if position == None:
                return -1
            else:
                return 1 + max(height_1(position.left), height_1(position.right))

        if position is None:
            position = self._root
        return height_1(position)  # start _height2 recursion

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        # height = self.height()
        return self.height() < 2*log(self._size + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [el for el in self.inorder() if low <= el <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def recurse(sequense):
            '''Take middle element to the tree until sequense be empty'''
            if sequense == []:
                return

            length = len(sequense)
            if length == 1:
                self.add(sequense[0])
                return

            middle = length//2
            self.add(sequense[middle])

            recurse(sequense[:middle])
            recurse(sequense[middle + 1:])

        all_agges = []
        for edge in self:
            all_agges.append(edge)

        all_agges.sort()
        self.clear()
        recurse(all_agges)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for el in self.inorder():
            if item < el:
                return el
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
        previous = None
        for el in self.inorder():
            if item <= el:
                return previous
            previous = el

        if previous < item:
            return previous
        return None

    def demo_bst(self, path, test_size=10000):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        list_of_words = []
        with open(path, 'r') as file:
            for line in file:
                list_of_words.append(line.strip())

        random.seed(77)
        random_list = [random.choice(list_of_words) for _ in range(test_size)]

        bst_sorted, bst_random, bst_balanced = LinkedBST(), LinkedBST(), LinkedBST()
        for word in sorted(random_list):
            bst_sorted.add(word)

        for word in random_list:
            bst_random.add(word)

        for word in random_list:
            bst_balanced.add(word)
        bst_balanced.rebalance()

        # now = time.time()
        # for word in random_list:
        #     word in random_list
        # print(f'Size of testing: {test_size}\n')
        # print(f'List time: {time.time() - now}\n')

        for bst in [(bst_sorted, 'Sorted tree'),
                    (bst_random, 'Random tree'),
                    (bst_balanced, 'Balanced tree')]:

            name = bst[1]
            now = time.time()
            for word in random_list:
                bst[0].find(word)
            print(f'{name} time: {time.time() - now}\n')

        return


if __name__ == '__main__':
    bst = LinkedBST()
    for el in [2, -1, 3, 4, -2, 6]:
        bst.add(el)
    # print(bst)
    # print(bst.height())
    # print(bst.is_balanced(), bst._size)
    # bst.rebalance()
    # print(bst)
    # a = bst.range_find(0, 7)
    # print(a)
    # print(bst.predecessor(9))
    a = bst.demo_bst('words.txt')
    # print(a[:10])
