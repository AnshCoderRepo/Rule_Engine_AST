import { useState } from 'react';
import { createRule, combineRules, evaluateRule } from '@/app/services/api';
import ASTTree from '@/app/components/ASTTree';

const Home = () => {
    const [rule, setRule] = useState('');
    const [ruleName, setRuleName] = useState('');
    const [combinedRules, setCombinedRules] = useState<string[]>([]);
    const [ast, setAst] = useState<any>(null);

    const handleCreateRule = async () => {
        const data = await createRule(rule, ruleName);
        setAst(data);
    };

    const handleCombineRules = async () => {
        const data = await combineRules(combinedRules);
        setAst(data);
    };

    return (
        <div>
            <h1>Rule Engine</h1>
            <div>
                <h2>Create Rule</h2>
                <input 
                    type="text" 
                    placeholder="Rule Name"
                    value={ruleName}
                    onChange={(e) => setRuleName(e.target.value)} 
                />
                <input 
                    type="text" 
                    placeholder="Rule"
                    value={rule}
                    onChange={(e) => setRule(e.target.value)} 
                />
                <button onClick={handleCreateRule}>Create Rule</button>
            </div>
            <div>
                <h2>Combine Rules</h2>
                {combinedRules.map((rule, index) => (
                    <input 
                        key={index} 
                        type="text" 
                        value={rule}
                        onChange={(e) => {
                            const newRules = [...combinedRules];
                            newRules[index] = e.target.value;
                            setCombinedRules(newRules);
                        }} 
                    />
                ))}
                <button onClick={() => setCombinedRules([...combinedRules, ''])}>
                    Add Rule
                </button>
                <button onClick={handleCombineRules}>Combine Rules</button>
            </div>
            <div>
                {ast && <ASTTree root={ast} />}
            </div>
        </div>
    );
};

export default Home;
