import os
from util import load_config, read_json, save_json
from lm_eval.api.instance import Instance
from lm_eval.filters import build_filter_ensemble
from lm_eval.api.registry import (
    AGGREGATION_REGISTRY,
    DEFAULT_METRIC_REGISTRY,
    get_aggregation,
    get_metric,
    get_metric_aggregation,
    is_higher_better,
)
from tqdm import tqdm

from argparse import ArgumentParser


def main(config, outdir):
    result_file = os.path.join(outdir, "results.json")
    results = read_json(result_file)
    prediction_key = config.get('prediction_key', 'prediction')
    filtered_key =  "filtered_"+prediction_key
    answer_key = config.get('answer_key', 'answer')
    _metric_list = config.get('metrics', [])
    _metric_fn_list = {}
    _metric_fn_kwargs = {}
    _metric_values = {}
    _agg_fn = {}
    for metric_config in _metric_list:
        metric_name = metric_config["metric"]
        _metric_fn_list[metric_name] = get_metric(metric_name)
        kwargs = {
                    key: metric_config[key]
                    for key in metric_config
                    if key
                    not in ["metric", "aggregation", "higher_is_better", "hf_evaluate"]
                }
        _metric_fn_kwargs[metric_name] = kwargs
        _agg_fn[metric_name] = get_aggregation(metric_config["aggregation"])
    filters = []
    for filter_config in config['filter_list']:
        filter_name = filter_config["name"]
        filter_functions = filter_config["filter"]
        components = []
        for function in filter_functions:
            kwargs = {
                key: function[key] for key in function if key != "function"
            }
            components.append([function["function"], kwargs])
        filter_pipeline = build_filter_ensemble(filter_name, components)
        filters.append(filter_pipeline)
    
    for i in tqdm(range(len(results))):
        pred = results[i][prediction_key]
        ans = results[i][answer_key]
        instance = Instance(
            request_type = None, # TODO
            doc = results[i],
            arguments = [],
            idx = i,
            resps = [pred],
        )
        for f in filters:
            f.apply([instance])
        results[i][filtered_key] = list(instance.filtered_resps.values())[0]
        for metric_config in _metric_list:
            metric_name = metric_config["metric"]
            pred = results[i][filtered_key]
            ans = results[i][answer_key]
            result_score = _metric_fn_list[metric_name](
                                references=[ans],
                                predictions=[pred],
                                **_metric_fn_kwargs[metric_name],
                            )
            results[i].update(result_score)
            if metric_name not in _metric_values:
                _metric_values[metric_name] = [result_score[metric_name]]
            else:
                _metric_values[metric_name].append(result_score[metric_name])
    
    for metric_name in _metric_values.keys():
        _metric_values[metric_name] = _agg_fn[metric_name](_metric_values[metric_name])
        print(f"{metric_name}({_agg_fn[metric_name].__name__}) : {_metric_values[metric_name] }")


    out_file = os.path.join(outdir, 'metrics_'+os.path.basename(result_file))
    save_json(results, out_file)
    
    out_file = os.path.join(outdir, 'metrics.json')
    save_json(_metric_values, out_file)

def parse_args():
    parser = ArgumentParser(description='Simple : Question Answer Chain')
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--outdir', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    config = load_config(args.config)
    # Calling the main function
    main(config, args.outdir)