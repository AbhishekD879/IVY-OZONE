const siteServer = require('../../lib/siteServer');

module.exports = function(req, res) {
  siteServer.getEvents(req.params.selectionType, req.params.selectionId, req.params.from, req.params.to)
    .then(
      result => {
        if (result) {
          res
            .status(200)
            .json(result)
            .end();
        } else {
          res.sendStatus(404);
          res.end();
        }
      },
      err => {
        res
          .status(500)
          .json({ error: 'error', detail: err ? err.message : '' })
          .end();
      }
    );
};
