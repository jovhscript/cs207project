from BinarySearchDatabase import ValueRef, BinaryNodeRef, BinaryNode, BinaryTree, Storage
import pickle
import os

class Color(object):
    """
    This class produces a color definition for a given node of interest.
    """
    RED = 0
    BLACK = 1

class RedBlackNodeRef(ValueRef):
    """
    This class produces a reference to a red-black binary search tree node on the disk.   
    """
    def __init__(self, referent=None, address=0):
        """
        The constructor of the class takes for arguments a referent and address
        
        Parameters
        ----------
        
        referent: value to store for the red-black tree node, optional
        address: target address for the red-black tree node value, optional
        
        Attributes
        ----------
        
        self._referent: value
        self._address: address
        """
        self._referent = referent #value to store
        self._address = address #address to store at

    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        """
        Method that stores refs for the node 
        
        Parameter
        ---------
        
        storage: a storage address at which the value is stored
        
        """
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """
        Method that uses pickle to convert the node to bytes
        
        Parameter
        ---------
        
        referent: the value to be stored in the node
        
        """
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'color': referent.color
        })

    @staticmethod
    def bytes_to_referent(string):
        """
        Method that unpickles bytes to obtain a node object
        
        Parameter
        ---------
        
        referent: the value to be stored in the node
        
        """
        d = pickle.loads(string)
        return RedBlackNode(
            RedBlackNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            RedBlackNodeRef(address=d['right']),
            d['color']
        )


class RedBlackNode(BinaryNode):

    @classmethod
    def from_node(cls, node, **kwargs):
        """
        Method that clones a node given changes from another node
        
        Parameters
        ----------
        
        node: the node whose properties will be emulated
        kwargs: obtain key, value, right and left refs to clone
        
        """
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color=kwargs.get('color', node.color),
        )

    def __init__(self, left_ref, key, value_ref, right_ref, color=Color.RED):
        """
        The constructor of the class takes for arguments the refs belonging to the node itself, its right child, its left child, and its key.
        
        Parameters
        ----------
        
        left_ref: reference for left node, mandatory
        key: the key value of the node, mandatory
        value_ref: reference for node, mandatory
        right_ref: reference for right node, mandatory
        
        Attributes
        ----------
        
        self.left_ref: ref address
        self.key: value
        self.value_ref: ref address
        self.right_ref: ref address
        
        """
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color = color

    def is_black(self):
        """
        Method to identify whether a particular node is black.
        """
        return self.color == Color.BLACK

    def is_red(self):
        """
        Method to identify whether a particular node is red.
        """
        return self.color == Color.RED

    def is_empty(self):
        """
        Method to identify whether a particular node is empty.
        """
        return False


class RedBlackTree(BinaryTree):

    def _refresh_tree_ref(self):
        """
        Method to get reference to new tree if it has changed
        
        """
        self._tree_ref = RedBlackNodeRef(
            address=self._storage.get_root_address())

    def is_empty(self):
        """
        Method to identify an empty tree.
        
        """
        return False

    def _blacken(self, node):
        """
        Method that sets a node's color to black unless the node is null
        
        Parameter
        ---------
        
        node: the node to be coloured black
        
        """
        #node = self._follow(ref)
        if node is None:
            return node
        newnode = RedBlackNode.from_node(node, color=Color.BLACK)
        return RedBlackNodeRef(newnode)

    def rootkey(self):
        """
        Method that collects the key of the tree's root.
        
        """
        return self._follow(self._tree_ref).key

    def rotate_left(self, node):
        """
        Method that rotates a node left. 
        
        Parameter
        ---------
        
        node: the node to be rotated
        
        Notes
        -----
        
        This method is invoked when a violation of the red-black rules is found, namely when two red nodes exist in succession.
        
        1) If the violated node's uncle node is red, this method is unnecessary as recoloring will rectify the violation.
        
        2) If the violated node's uncle node is a black, but the violated node is the right child of a left node, this method is necessary.
        The rotation entails moving the child node up to the position of the parent node, and then making the parent node the left child of the 
        original child node. The original child node's left subtree, if it exists, is passed as a right subtree to the new left-child.
        
        3) If the violated node's uncle node is a black, but the violated node is the right child of a right node, this method is also necessary.
        The rotation entails making the parent node a left-child of the grandparent, replacing the grandparent with the parent, and moving the 
        node to its parent's position. The left subtree of the original parent becomes a right subtree of the grandparent in its new position
        The colors are also recalibrated with the parent set to black and the grandparent and original node set to red.    
        
        
        """    
        
        right = self._follow(node.right_ref)
        if self._follow(right.left_ref) is not None:
            newleft_right = RedBlackNode.from_node(self._follow(right.left_ref),
                                                   left_ref = RedBlackNodeRef(),
                                                   right_ref = RedBlackNodeRef(),
                                                   color = node.color)
            newleft_right_ref = RedBlackNodeRef(referent = newleft_right)
        else:
            newleft_right_ref = RedBlackNodeRef()
        newleft = RedBlackNode.from_node(node, 
                                         right_ref = newleft_right_ref)
        newnode = RedBlackNode.from_node(right,
                                         left_ref = RedBlackNodeRef(referent=newleft))
        return newnode


    def rotate_right(self, node):
        
        """
        Method that rotates a node right. 
    
        Parameter
        ---------
        
        node: the node to be rotated
        
        Notes
        -----
        
        This method is invoked when a violation of the red-black rules is found, namely when two red nodes exist in succession.
        
        1) If the violated node's uncle node is red, this method is unnecessary as recoloring will rectify the violation.
        
        2) If the violated node's uncle node is a black, but the violated node is the left child of a right node, this method is necessary.
        The rotation entails moving the child node up to the position of the parent node, and then making the parent node the right child of the 
        original child node. The original child node's right subtree, if it exists, is passed as a left subtree to the new right-child.
        
        3) If the violated node's uncle node is a black, but the violated node is the left child of a left node, this method is also necessary.
        The rotation entails making the parent node a right-child of the grandparent, replacing the grandparent with the parent, and moving the 
        node to its parent's position. The right subtree of the original parent becomes a left subtree of the grandparent in its new position
        The colors are also recalibrated with the parent set to black and the grandparent and original node set to red.    
        
        
        """
        left = self._follow(node.left_ref)
        if self._follow(left.right_ref) is not None:
            newright_left = RedBlackNode.from_node(self._follow(left.right_ref),
                                                   left_ref = RedBlackNodeRef(),
                                                   right_ref = RedBlackNodeRef(),
                                                   color = node.color)
            newright_left_ref = RedBlackNodeRef(referent = newright_left)
        else:
            newright_left_ref = RedBlackNodeRef()
                                        
        newright = RedBlackNode.from_node(node, 
                                          left_ref = newright_left_ref)
        newnode = RedBlackNode.from_node(left,
                                         right_ref = RedBlackNodeRef(referent=newright))

        return newnode
                                      
    def recolor(self, node):
    
        """
        Method that recolours a node by setting its leaves to black and set it to red.
        
        Parameter
        ---------
        
        node: the node to be recoloured.
        
        """
        
        left = self._blacken(self._follow(node.left_ref))
        right = self._blacken(self._follow(node.right_ref))

        return RedBlackNode.from_node(node, 
                                      left_ref = left,
                                      right_ref = right,
                                      color=Color.RED)

    def _isred(self, node):
        """
        Method that identifies whether a given node is red
        
        Parameter
        ---------
        
        node: the node to be checked.
        
        """
        
        if node is None:
            return False
        else:
            return node.color == Color.RED

    def balance(self, node):
        """
        Method that balances a tree given a new node. This is done by recoloring and rotating necessary sections of the tree.
        
        Parameter
        ---------
        
        node: the node that has been recently modified or inserted.
        
        """
        
        if self._isred(node) | (node is None):
            return node

        left = self._follow(node.left_ref)
        right = self._follow(node.right_ref)

        if self._isred(left):
            if self._isred(right):
                return self.recolor(node)
            if self._isred(self._follow(left.left_ref)):
                return self.recolor(self.rotate_right(node))
            if self._isred(self._follow(left.right_ref)):
                newleft = self.rotate_left(left)
                newnode = RedBlackNode.from_node(node, 
                                                 left_ref = RedBlackNodeRef(referent = newleft))
                return self.recolor(self.rotate_right(newnode))
        if self._isred(right):
            if self._isred(self._follow(right.right_ref)):
                return self.recolor(self.rotate_left(node))
            if self._isred(self._follow(right.left_ref)):
                newright = self.rotate_right(right)
                newnode = RedBlackNode.from_node(node, 
                                                 right_ref = RedBlackNodeRef(referent = newright))
                return self.recolor(self.rotate_left(newnode))

        return node

    def set(self, key, value):
        """
        Method that sets a new value in the tree. Since the tree is immutable, a new tree is created.
        
        Parameters
        ----------
        
        key: a lookup value
        value: the value that will be stored for the key
        
        """
        #try to lock the tree. If we succeed make sure
        #we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        #get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        #insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)
        self._tree_ref = self._blacken(self._follow(self._tree_ref))


    def _insert(self, node, key, value_ref):
        """
        Method that inserts a new node, creating a new path from tree's root.
        
        Parameters
        ----------
        
        key: a lookup value
        node: address
        value_ref: the reference address of the new node as per its new path from the tree root
        
        """
        #create a tree if there was none so far
        if node is None:
            #print ('a')
            new_node = RedBlackNode(
               RedBlackNodeRef(), key, value_ref, RedBlackNodeRef())
        elif key < node.key:
            newleft_ref = self._insert(self._follow(node.left_ref), key, value_ref)
            newleft = self.balance(self._follow(newleft_ref))
            new_node = self.balance(RedBlackNode.from_node(
                    node,
                    left_ref=RedBlackNodeRef(referent=newleft)))
        elif key > node.key:
            newright_ref = self._insert(self._follow(node.right_ref), key, value_ref)
            newright = self.balance(self._follow(newright_ref))
            new_node = self.balance(RedBlackNode.from_node(
                    node,
                    right_ref=RedBlackNodeRef(referent=newright)))
        else: #create a new node to represent this data
            new_node = RedBlackNode.from_node(node, value_ref=value_ref)
        #new_node = self._blacken(new_node)
        return RedBlackNodeRef(referent=new_node)


def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return DBDB(f)


class DBDB(object):

    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = RedBlackTree(self._storage)

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        self._storage.close()

    def commit(self):
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        self._assert_not_closed()
        return self._tree.get(key)

    def set(self, key, value):
        self._assert_not_closed()
        return self._tree.set(key, value)

    def getRootKey(self):
        return self._tree.rootkey()

    def delete(self, key):
        self._assert_not_closed()
        return self._tree.delete(key)
    def get_nodes_less_than(self, key):
        self._assert_not_closed()
        return self._tree.get_nodes_less_than(key)
    
    def get_nodes_greater_than(self, key):
        self._assert_not_closed()
        return self._tree.get_nodes_greater_than(key)   
    
    def in_order_traversal(self):
        self._assert_not_closed()
        return self._tree.in_order_traversal()        
