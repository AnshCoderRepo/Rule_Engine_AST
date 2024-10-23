import React from 'react';
import { Tree, TreeNodeDatum } from 'react-d3-tree';

interface ASTNode {
    node_type: string;
    left?: ASTNode;
    right?: ASTNode;
    value?: any;
}

interface ASTTreeProps {
    root: ASTNode;
}

const convertToTreeNode = (node: ASTNode): TreeNodeDatum => {
    const treeNode = {
        name: node.node_type,
        attributes: node.value ? { ...node.value } : {},
    } as TreeNodeDatum;

    const children: TreeNodeDatum[] = [];
    if (node.left) {
        children.push(convertToTreeNode(node.left));
    }
    if (node.right) {
        children.push(convertToTreeNode(node.right));
    }
    if (children.length > 0) {
        treeNode.children = children;
    }

    return treeNode;
};

const ASTTree: React.FC<ASTTreeProps> = ({ root }) => {
    const treeData = [convertToTreeNode(root)];
    return (
        <div style={{ width: '100%', height: '500px' }}>
            <Tree data={treeData} orientation="vertical" />
        </div>
    );
};

export default ASTTree;