define(['knockout', 'underscore'], function (ko, _) {
    return ko.components.register('text-widget', {
        viewModel: function(params) {
            this.value = params.value;
            _.extend(this, _.pick(params.config, 'label', 'placeholder'));
        },
        template: { require: 'text!widget-templates/text' }
    });
});