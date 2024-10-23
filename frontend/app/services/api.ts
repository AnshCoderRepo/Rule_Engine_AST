import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export const createRule = async (rule: string, name: string) => {
    const response = await axios.post(`${API_URL}/create_rule`, { rule, name });
    return response.data;
};

export const combineRules = async (rules: string[]) => {
    const response = await axios.post(`${API_URL}/combine_rules`, { rules });
    return response.data;
};

export const evaluateRule = async (ruleId: number, data: Record<string, any>) => {
    const response = await axios.post(`${API_URL}/evaluate_rule`, { rule_id: ruleId, data });
    return response.data;
};